from src.core.consts import MAX_NOTE_HOLD_TIME, MIN_SLIDER_END_RELEASE_TIME, MAX_SLIDER_END_RELEASE_TIME, \
    ROUND_DIGIT_COUNT, EDGE_DISTANCE, ADJUSTED_UR


class CoreSettings:
    def __init__(self):
        self.MAX_NOTE_HOLD_TIME = MAX_NOTE_HOLD_TIME
        self.MIN_SLIDER_END_RELEASE_TIME = MIN_SLIDER_END_RELEASE_TIME
        self.MAX_SLIDER_END_RELEASE_TIME = MAX_SLIDER_END_RELEASE_TIME

        self.ROUND_DIGIT_COUNT = ROUND_DIGIT_COUNT
        self.EDGE_DISTANCE = EDGE_DISTANCE
        self.ADJUSTED_UR = ADJUSTED_UR
        self.OSU_FOLDER = None

    def re_init(
            self,
            max_note_hold_time=None,
            min_slider_end_release_time=None,
            max_slider_end_release_time=None,

            round_digit_count=None,
            edge_distance=None,
            adjusted_ur=None,
            osu_folder=None,
    ):
        self.MAX_NOTE_HOLD_TIME = max_note_hold_time or self.MAX_NOTE_HOLD_TIME
        self.MIN_SLIDER_END_RELEASE_TIME = min_slider_end_release_time or self.MIN_SLIDER_END_RELEASE_TIME
        self.MAX_SLIDER_END_RELEASE_TIME = max_slider_end_release_time or self.MAX_SLIDER_END_RELEASE_TIME

        self.ROUND_DIGIT_COUNT = round_digit_count or self.ROUND_DIGIT_COUNT
        self.EDGE_DISTANCE = edge_distance or self.EDGE_DISTANCE
        self.ADJUSTED_UR = adjusted_ur or self.ADJUSTED_UR
        self.OSU_FOLDER = osu_folder or self.OSU_FOLDER
