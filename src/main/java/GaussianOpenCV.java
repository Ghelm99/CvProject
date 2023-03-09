import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

public class GaussianOpenCV {

	public static void main(String[] args) {

		nu.pattern.OpenCV.loadLocally();

		/* Load the image */
		Mat input = Imgcodecs.imread("images/input.jpg");

		/* Apply a Gaussian filter with a kernel size of 5 and a sigma value of 1 */
		Mat output = new Mat();
		Imgproc.GaussianBlur(input, output, new Size(5, 5), 1.0);

		/* Save the filtered image */
		Imgcodecs.imwrite("images/output.jpg", output);
	}
}
