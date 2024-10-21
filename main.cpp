#include <iostream>
#include <opencv2/opencv.hpp>
#include "src/yolo.h"


int main(int argc, char const *argv[]) {



    if (argc != 2) {
      std::cout << "Usage: " << argv[0] << " <model_path>" << std::endl;
      return 1;
    }


    cv::VideoCapture cap(0);

    InferenceEngine engine(argv[1]);


    while (true) {

        cv::Mat frame;
        cap >> frame;


        int orig_width = frame.cols;
        int orig_height = frame.rows;
        auto timer = cv::getTickCount();

        std::vector<float> input_tensor_values = engine.preprocessImage(frame);

        std::vector<float> results = engine.runInference(input_tensor_values);

        float confidence_threshold = 0.3;

        std::vector<Detection> detections = engine.filterDetections(results, confidence_threshold, engine.input_shape[2], engine.input_shape[3], orig_width, orig_height);

        double fps = cv::getTickFrequency() / ((double)cv::getTickCount() - timer);

        cv::putText(frame, "FPS: " + std::to_string(fps), cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 255, 0), 2, 8);

        cv::Mat output = engine.draw_labels(frame, detections);


        cv::imshow("Video", frame);
        if (cv::waitKey(30) & 0xFF == 27) {
            break;
        }


    }

    return 0;
}
