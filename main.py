from enum import Enum
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from bistro_beacon.config import CoreSettings
from bistro_beacon.core.storage import FrameStorageType
from bistro_beacon.core.visualization.config import BaseVisualizationConfig
from bistro_beacon.core.context.base import StreamContext

class VideoCaptureBackend(str, Enum):
    FFMPEG = "ffmpeg"
    GSTREAMER = "gstreamer"

class HandRaiseSettings(BaseSettings, BaseVisualizationConfig):
    settings: CoreSettings = Field()
    stream_context: StreamContext = Field(default_factory=StreamContext)

    weights: str = Field(default="../models/yolo11x-pose.pt")
    source: str = Field(default="0")
    device: str = Field(default="0")
    
    video_capture_backend: VideoCaptureBackend = Field(default=VideoCaptureBackend.FFMPEG)
    gst_pipeline_template: str = Field(
        default=(
            'rtspsrc location="{source}" latency=0 buffer-mode=auto ! '
            'queue max-size-buffers=300 ! '
            'decodebin ! '
            'videoconvert ! '
            'video/x-raw,format=BGR ! '
            'appsink max-buffers=1 drop=True sync=false async=false'
        )
    )
    fps_limit: Optional[float] = Field(default=6.0)
    view_img: bool = Field(default=True)
    line_thickness: int = Field(default=2)
    
    storage_type: FrameStorageType = Field(default=FrameStorageType.LOCAL)
    output_dir: str = Field(default="../runs/hand_raise")

    tracker: str = Field(default="botsort.yaml")
    cleanup_interval: float = Field(default=30.0)
    max_track_age: float = Field(default=30.0)
    process_all_frames: bool = Field(default=False)
    stay_check_interval: float = Field(default=1.0)
    stay_confirmation_threshold: float = Field(default=2.0)

    def get_gst_pipeline(self) -> str:
        return self.gst_pipeline_template.format(source=self.source)

    class Config:
        env_prefix = "HAND_RAISE_"
        extra = "allow"
        env_file = ".env"