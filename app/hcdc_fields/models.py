from ..extensions import BaseDB, db

class CourtDivisionIndicator(BaseDB):
    
    # tablename
    __tablename__ = 'court_division_indicator'
    
    # table columns
    code                                    = db.Column(db.Integer, unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
class InstrumentType(BaseDB):
    
    # tablename
    __tablename__ = 'instrument_type'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(3), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass

class CaseDisposition(BaseDB):
    
    # tablename
    __tablename__ = 'case_disposition'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(4), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
class CaseStatus(BaseDB):
    
    # tablename
    __tablename__ = 'case_status'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(1), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
class DefendantStatus(BaseDB):
    
    # tablename
    __tablename__ = 'defendant_status'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(1), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
class CurrentOffenseLevelDegree(BaseDB):
    
    # tablename
    __tablename__ = 'current_offense_level_degree'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(2), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass

class DocketCalendarName(BaseDB):
    
    # tablename
    __tablename__ = 'docket_calendar_name'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(3), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass

class CalendarReason(BaseDB):
    
    # tablename
    __tablename__ = 'calendar_reason'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(4), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
class DefendantRace(BaseDB):
    
    # tablename
    __tablename__ = 'defendant_race'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(1), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass