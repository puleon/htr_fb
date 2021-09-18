import logging
import time

from path import Path
from flask import Flask, request, jsonify
from healthcheck import HealthCheck
import sentry_sdk

from model import Model, DecoderType
from main_fb import FilePaths, predict


logger = logging.getLogger(__name__)

app = Flask(__name__)
health = HealthCheck(app, "/healthcheck")
logging.getLogger("werkzeug").setLevel("WARNING")

decoder_mapping = {'bestpath': DecoderType.BestPath,
                    'beamsearch': DecoderType.BeamSearch,
                    'wordbeamsearch': DecoderType.WordBeamSearch}

decoder_type = decoder_mapping['bestpath']

model = Model(list(open(FilePaths.fn_char_list).read()), decoder_type, must_restore=True, dump=False)
 


@app.route("/respond", methods=["POST"])
def respond():
    st_time = time.time()

    image = request.json.get("image", "")
    min_confidence = request.json.get("min_confidence", 0)

    logger.info(f"got request: image={image}, min_confidence={min_confidence}")

    fn_img = Path(image)

    try:
        result = predict(model, fn_img=fn_img)
    except Exception as exc:
        logger.exception(exc)
        sentry_sdk.capture_exception(exc)
        result = []

    total_time = time.time() - st_time
    logger.info(f"zero-shot object detection exec time: {total_time:.3f}s")
    return jsonify(result["recognized"])