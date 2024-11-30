#include <iostream>
#include <opencv2/opencv.hpp>


int main(int argc, char const *argv[]) {


    if (argc != 2) {
      std::cout << "Usage: " << argv[0] << " <model_path>" << std::endl;
      return 1;
    }

    cv::VideoCapture cap(0);


    while (true) {

        cv::Mat frame;
        cap >> frame;


        if (std::getenv("DEBUG") != NULL) {
            cv::imshow("Video", frame);
        }


        if (cv::waitKey(1) == 'q') {
            break;
        }


    }


    cap.release();

    cv::destroyAllWindows();

    return 0;
}
