import argparse
import os
import shutil
import time
from pathlib import Path

import cv2
import torch
from numpy import random
from torch.backends import cudnn

from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import LoadImages, LoadStreams
from yolov5.utils.general import (
    apply_classifier,
    check_img_size,
    non_max_suppression,
    plot_one_box,
    scale_coords,
    set_logging,
    strip_optimizer,
    xyxy2xywh,
)
from yolov5.utils.torch_utils import load_classifier, select_device, time_synchronized


# Load Ground Truth
def load_ground_truth(label_path, img_shape):
    print(f"Loading label file: {label_path}")  # Add this line to debug
    ground_truth_boxes = []
    if os.path.exists(label_path):
        with open(label_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                cls, x_center, y_center, width, height = map(
                    float, line.strip().split()
                )
                # process the labels as expected
                ground_truth_boxes.append((cls, x_center, y_center, width, height))
    return ground_truth_boxes


def detect(save_img=False):
    out, source, weights, view_img, save_txt, imgsz = (
        opt.output,
        opt.source,
        opt.weights,
        opt.view_img,
        opt.save_txt,
        opt.img_size,
    )
    webcam = (
        source.isnumeric()
        or source.startswith(("rtsp://", "rtmp://", "http://"))
        or source.endswith(".txt")
    )

    # Initialize
    set_logging()
    device = select_device(opt.device)
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    half = device.type != "cpu"  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name="resnet101", n=2)  # initialize
        modelc.load_state_dict(
            torch.load("weights/resnet101.pt", map_location=device)["model"]
        )  # load weights
        modelc.to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, "module") else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != "cpu" else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Load Ground Truth
        # Convert to label path by replacing 'images' with 'labels' and changing the
        # extension to .txt
        label_path = str(
            Path(path).parent.joinpath(
                path.replace("images", "labels").replace(".jpg", ".txt")
            )
        )
        ground_truth_boxes = load_ground_truth(label_path, im0s.shape)  # Load GT boxes

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # print("Raw predictions:")
        # print(pred)

        # Apply NMS
        pred = non_max_suppression(
            pred,
            opt.conf_thres,
            opt.iou_thres,
            classes=opt.classes,
            agnostic=opt.agnostic_nms,
        )
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0 = path[i], f"{i}: ", im0s[i].copy()
            else:
                p, s, im0 = path, "", im0s

            save_path = str(Path(out) / Path(p).name)
            txt_path = str(Path(out) / Path(p).stem) + (
                "_%g" % dataset.frame if dataset.mode == "video" else ""
            )
            s += "%gx%g " % img.shape[2:]  # print string

            # Draw Ground Truth boxes
            height, width = im0s.shape[:2]  # 获取图像的实际高度和宽度
            for cls, x_center, y_center, w, h in ground_truth_boxes:
                # 将YOLO的相对坐标转换为实际像素坐标
                x1 = int((x_center - w / 2) * width)  # 左上角x坐标
                y1 = int((y_center - h / 2) * height)  # 左上角y坐标
                x2 = int((x_center + w / 2) * width)  # 右下角x坐标
                y2 = int((y_center + h / 2) * height)  # 右下角y坐标

                # 在图像上绘制矩形框
                cv2.rectangle(
                    im0, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2
                )  # 蓝色矩形框
                label = f"GT {names[int(cls)]}"  # 添加标签
                cv2.putText(
                    im0,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    thickness=1,
                )

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += "%g %ss, " % (n, names[int(c)])  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (
                            (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                            .view(-1)
                            .tolist()
                        )  # normalized xywh
                        with open(txt_path + ".txt", "a") as f:
                            f.write(("%g " * 5 + "\n") % (cls, *xywh))  # label format

                    if save_img or view_img:  # Add bbox to image
                        label = "%s %.2f" % (names[int(cls)], conf)
                        plot_one_box(
                            xyxy,
                            im0,
                            label=label,
                            color=colors[int(cls)],
                            line_thickness=3,
                        )

            # Print time (inference + NMS)
            print("%sDone. (%.3fs)" % (s, t2 - t1))

            # Stream results
            if view_img:
                cv2.imshow(p, im0)
                if cv2.waitKey(1) == ord("q"):  # q to quit
                    raise StopIteration

            # Save results (image with detections)
            if save_img:
                if dataset.mode == "images":
                    cv2.imwrite(save_path, im0)
                else:
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = "mp4v"  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(
                            save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h)
                        )
                    vid_writer.write(im0)

    if save_txt or save_img:
        print("Results saved to %s" % Path(out))

    print("Done. (%.3fs)" % (time.time() - t0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights", nargs="+", type=str, default="yolov5s.pt", help="model.pt path(s)"
    )
    parser.add_argument(
        "--source", type=str, default="inference/images", help="source"
    )  # file/folder, 0 for webcam
    parser.add_argument(
        "--output", type=str, default="inference/output", help="output folder"
    )  # output folder
    parser.add_argument(
        "--img-size", type=int, default=640, help="inference size (pixels)"
    )
    parser.add_argument(
        "--conf-thres", type=float, default=0.4, help="object confidence threshold"
    )
    parser.add_argument(
        "--iou-thres", type=float, default=0.5, help="IOU threshold for NMS"
    )
    parser.add_argument(
        "--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu"
    )
    parser.add_argument("--view-img", action="store_true", help="display results")
    parser.add_argument("--save-txt", action="store_true", help="save results to *.txt")
    parser.add_argument(
        "--classes",
        nargs="+",
        type=int,
        help="filter by class: --class 0, or --class 0 2 3",
    )
    parser.add_argument(
        "--agnostic-nms", action="store_true", help="class-agnostic NMS"
    )
    parser.add_argument("--augment", action="store_true", help="augmented inference")
    parser.add_argument("--update", action="store_true", help="update all models")
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ["yolov5s.pt", "yolov5m.pt", "yolov5l.pt", "yolov5x.pt"]:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()
