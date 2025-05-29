class CameraController:
    def __init__(self, camera_service):
        self.camera_service = camera_service

    def capture_image(self):
        return self.camera_service.capture_image()

    def start_video_stream(self):
        return self.camera_service.start_video_stream()

    def stop_video_stream(self):
        return self.camera_service.stop_video_stream()