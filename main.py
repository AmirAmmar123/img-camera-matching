from cameraImageMatcher import CameraImageMatcher

if __name__ == '__main__':
    args = CameraImageMatcher.parse_arguments()
    matcher = CameraImageMatcher(args)
    matcher.run()
