class Steps:

    step: float = 0.000001
    is_longitude_tiling = False

    @staticmethod
    def step_right(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_right(longitude + Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_left(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_left(longitude - Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_up(latitude: float, longitude: float) -> dict:
        latitude = Steps.check_sign_latitude(latitude + Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_down(latitude: float, longitude: float) -> dict:
        latitude = Steps.check_sign_latitude(latitude - Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_up_right(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_right(longitude + Steps.step)
        latitude = Steps.check_sign_latitude(latitude + Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_up_left(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_right(longitude - Steps.step)
        latitude = Steps.check_sign_latitude(latitude + Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_down_right(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_right(longitude + Steps.step)
        latitude = Steps.check_sign_latitude(latitude - Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def step_down_left(latitude: float, longitude: float) -> dict:
        longitude = Steps.check_sign_longitude_right(longitude - Steps.step)
        latitude = Steps.check_sign_latitude(latitude - Steps.step)
        return {
                "latitude": latitude,
                "longitude": longitude
                }

    @staticmethod
    def check_sign_longitude_right(longitude: float) -> float:
        if longitude > 180 and not Steps.is_longitude_tiling:
            return -360 + longitude
        return  longitude

    @staticmethod
    def check_sign_longitude_left(longitude: float) -> float:
        if longitude < -180 and not Steps.is_longitude_tiling:
            return +360 - longitude
        return longitude

    @staticmethod
    def check_sign_latitude(latitude: float) -> float:
        if latitude > 90:
            return 90
        elif latitude < -90:
            return -90
        return latitude
