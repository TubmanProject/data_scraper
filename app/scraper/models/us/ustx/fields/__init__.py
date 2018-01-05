"""Harris County District Court Fields package."""
from .models import (CourtDivisionIndicator,
                     InstrumentType,
                     CaseDisposition,
                     CaseStatus,
                     DefendantStatus,
                     CurrentOffenseLevelDegree,
                     DocketCalendarName,
                     CalendarReason,
                     DefendantRace,
                     DefendantBirthplace,
                     DefendantUSCitizen)


def initialize_fields(data_path):
    """Initialize the fields."""
    CourtDivisionIndicator.setup_schema()
    InstrumentType.setup_schema()
    CaseDisposition.setup_schema()
    CaseStatus.setup_schema()
    DefendantStatus.setup_schema()
    CurrentOffenseLevelDegree.setup_schema()
    DocketCalendarName.setup_schema()
    CalendarReason.setup_schema()
    DefendantRace.setup_schema()
    DefendantBirthplace.setup_schema()
    DefendantUSCitizen.setup_schema()
    CourtDivisionIndicator.seed_db(data_path)
    InstrumentType.seed_db(data_path)
    CaseDisposition.seed_db(data_path)
    CaseStatus.seed_db(data_path)
    DefendantStatus.seed_db(data_path)
    CurrentOffenseLevelDegree.seed_db(data_path)
    DocketCalendarName.seed_db(data_path)
    CalendarReason.seed_db(data_path)
    DefendantRace.seed_db(data_path)
    DefendantBirthplace.seed_db(data_path)
    DefendantUSCitizen.seed_db(data_path)
