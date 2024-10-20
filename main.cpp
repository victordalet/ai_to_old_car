#include <iostream>
#include <opencv2/opencv.hpp>


int main() {
    cv::VideoCapture cap(0);

    while (true) {

        cv::Mat frame;
        cap >> frame;

        cv::imshow("Video", frame);
        if (cv::waitKey(30) & 0xFF == 27) {
            break;
        }


    }

    return 0;
}
