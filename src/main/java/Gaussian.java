import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

/* The code performs Gaussian filtering on an input image using a 2D kernel. */

public class Gaussian {

  public static void main(String[] args) throws IOException {

    /* Read input image and create output image */
    BufferedImage input = ImageIO.read(new File("images/input.jpg"));
    BufferedImage output = new BufferedImage(input.getWidth(), input.getHeight(), BufferedImage.TYPE_INT_RGB);

    /* Set kernel size and standard deviation for Gaussian blur */
    int kernelSize = 5;
    double sigma = 1.5;

    /* Create and initializing the Gaussian kernel */
    double[][] kernel = new double[kernelSize][kernelSize];
    double mean = kernelSize / 2;
    double sum = 0.0;
    for (int i = 0; i < kernelSize; i++) {
        for (int j = 0; j < kernelSize; j++) {
            kernel[i][j] = Math.exp(-0.5 * (Math.pow((i - mean) / sigma, 2.0) + Math.pow((j - mean) / sigma, 2.0))) / (2 * Math.PI * sigma * sigma);
            sum += kernel[i][j];
        }
    }

    /* Normalize the kernel */
    for (int i = 0; i < kernelSize; i++) {
        for (int j = 0; j < kernelSize; j++) {
            kernel[i][j] /= sum;
        }
    }

    /* Loop through each pixel in the input image */
    for (int i = 0; i < input.getWidth(); i++) {
        for (int j = 0; j < input.getHeight(); j++) {
            /* Initialize the color values */
            double red = 0.0;
            double green = 0.0;
            double blue = 0.0;
            /* Convolve the kernel around the pixel */
            for (int ki = 0; ki < kernelSize; ki++) {
                for (int kj = 0; kj < kernelSize; kj++) {
                    /* Compute index of the pixel */
                    int pi = i - kernelSize / 2 + ki;
                    int pj = j - kernelSize / 2 + kj;
                    /* Check if pixel is inside of the image */
                    if (pi >= 0 && pi < input.getWidth() && pj >= 0 && pj < input.getHeight()) {
                        /* Get the color of pixel at the current index */
                        Color color = new Color(input.getRGB(pi, pj));
                        /* Apply the kernel to the color values */
                        red += color.getRed() * kernel[ki][kj];
                        green += color.getGreen() * kernel[ki][kj];
                        blue += color.getBlue() * kernel[ki][kj];
                    }
                }
            }

            /* Round color values to integers and clamping them to 0-255 range */
            int filteredRed = (int) Math.round(red);
            int filteredGreen = (int) Math.round(green);
            int filteredBlue = (int) Math.round(blue);
            filteredRed = Math.min(filteredRed, 255);
            filteredGreen = Math.min(filteredGreen, 255);
            filteredBlue = Math.min(filteredBlue, 255);

            /* Set the color of pixel at the current index */
            output.setRGB(i, j, new Color(filteredRed, filteredGreen, filteredBlue).getRGB());
        }
    }

    /* Write the output image to file */
    ImageIO.write(output, "jpg", new File("images/output.jpg"));
  }
}
