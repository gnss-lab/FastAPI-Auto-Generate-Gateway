import os
import sys
import glob
from loguru import logger


class DeleteTmpModelsFilesUsecase:
    """The usecase designed for deleting temporary pydantic models.
    """

    def __init__(self) -> None:
        pass

    def execute(self):
        """Launch execution of usecase
        """
        project_root = os.path.dirname(
            sys.modules['fastapi_gateway_auto_generate'].__file__)

        filelist = glob.glob(os.path.join(
            f"{project_root}/tmp/models", "model_*"))
        for f in filelist:
            logger.debug(f)
            os.remove(f)
