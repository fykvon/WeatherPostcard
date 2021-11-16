import cv2

image_cv2 = cv2.imread('probe.jpg')


class ImageMaker:
    """
    Create image

    """

    def __init__(self, weather_data):

        self.name_of_window = 'postcard'
        self.weather_data = weather_data

    def make_gradient(self):
        image = image_cv2
        i = 0
        k = 0
        for _ in range(50):
            image[:, 0 + i:50 + i] = (50 + k, 255 - k / 8, 238)
            i += 20
            k += 5
        return image

    def make_images(self, day_information: list):
        """
        This method should get a list with weather information and create an image with gradient

        :param day_information: list
        :return: None
        """
        info_weather = day_information[0]
        self.make_gradient()
        y0, dy = 50, 20
        for i, param in enumerate(day_information):
            y = y0 + i * dy
            cv2.putText(image_cv2, param, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        self.gradient_maker(info_weather)

    def gradient_maker(self, info_weather: str):
        """
        This method gets a day information and creates a gradient on postcard

        :param info_weather: str
        :return: None
        """
        if 'Snow' in info_weather:
            self.gradient(weather_detail=cv2.WINDOW_NORMAL)
        if 'snow' in info_weather:
            self.gradient(weather_detail=cv2.WINDOW_NORMAL)
        if 'Clear' in info_weather:
            self.gradient(weather_detail=cv2.COLOR_BGR2RGB)
        if 'rain' in info_weather:
            self.gradient(cv2.COLOR_BGR2GRAY)
        if 'cloudy' in info_weather:
            self.gradient(weather_detail=cv2.COLOR_BGR2YUV)
        if 'Overcast' in info_weather:
            self.gradient(weather_detail=cv2.COLOR_BGR2YUV)

    def gradient(self, weather_detail: str):
        image = cv2.cvtColor(image_cv2, weather_detail)
        cv2.imshow('image', image)
        cv2.waitKey(0)

    def main(self):
        self.make_images(self.weather_data)
