import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;
import java.io.IOException;

public class GaussianMain {

	public static void main(String[] args) throws IOException {
		// Load the image
		BufferedImage image = ImageIO.read(new File("images/input.jpg"));

		// Create a new BufferedImage object for the filtered image
		BufferedImage filteredImage = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_RGB);

		// Define the kernel size and standard deviation
		int kernelSize = 5;
		double sigma = 1.5;

		// Create the kernel
		double[][] kernel = new double[kernelSize][kernelSize];
		double mean = kernelSize / 2;
		double sum = 0.0;
		for (int x = 0; x < kernelSize; ++x) {
			for (int y = 0; y < kernelSize; ++y) {
				kernel[x][y] = Math.exp(-0.5 * (Math.pow((x - mean) / sigma, 2.0) + Math.pow((y - mean) / sigma, 2.0))) / (2 * Math.PI * sigma * sigma);
				sum += kernel[x][y];
			}
		}

		// Normalize the kernel
		for (int x = 0; x < kernelSize; ++x) {
			for (int y = 0; y < kernelSize; ++y) {
				kernel[x][y] /= sum;
			}
		}

		// Apply the filter
		for (int x = 0; x < image.getWidth(); ++x) {
			for (int y = 0; y < image.getHeight(); ++y) {
				// Convolve the kernel with the image pixel values
				double red = 0.0;
				double green = 0.0;
				double blue = 0.0;
				for (int kx = 0; kx < kernelSize; ++kx) {
					for (int ky = 0; ky < kernelSize; ++ky) {
						int px = x - kernelSize / 2 + kx;
						int py = y - kernelSize / 2 + ky;
						if (px >= 0 && px < image.getWidth() && py >= 0 && py < image.getHeight()) {
							Color color = new Color(image.getRGB(px, py));
							red += color.getRed() * kernel[kx][ky];
							green += color.getGreen() * kernel[kx][ky];
							blue += color.getBlue() * kernel[kx][ky];
						}
					}
				}

				// Set the filtered pixel value in the output image
				int filteredRed = (int) Math.round(red);
				int filteredGreen = (int) Math.round(green);
				int filteredBlue = (int) Math.round(blue);
				filteredRed = Math.min(filteredRed, 255);
				filteredGreen = Math.min(filteredGreen, 255);
				filteredBlue = Math.min(filteredBlue, 255);
				filteredImage.setRGB(x, y, new Color(filteredRed, filteredGreen, filteredBlue).getRGB());
			}
		}

		// Save the filtered image
		ImageIO.write(filteredImage, "jpg", new File("images/output.jpg"));
	}
}