import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

public class GaussianMainWithOpencv {

	public static void main(String[] args) {

		nu.pattern.OpenCV.loadLocally();

		// Load the image
		Mat image = Imgcodecs.imread("images/input.jpg");

		// Apply a Gaussian filter with a kernel size of 5x5 and a sigma value of 1.0
		Mat filteredImage = new Mat();
		Imgproc.GaussianBlur(image, filteredImage, new Size(5, 5), 1.0);

		// Save the filtered image
		Imgcodecs.imwrite("images/output.jpg", filteredImage);

	}

}
