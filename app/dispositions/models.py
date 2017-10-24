from ..extensions import BaseDB, db

class Dispositions(BaseDB):
    
    # tablename
    __tablename__ = 'dispositions'
    
    # table columns
    rundate                                 = db.Column(db.DateTime, nullable=False)
    court_division_indicator_code           = db.Column(db.Integer, db.ForeignKey('court_division_indicator.code'), nullable=False)
    case_number                             = db.Column(db.Integer, nullable=False)
    filing_date                             = db.Column(db.DateTime, nullable=True)
    instrument_type_code                    = db.Column(db.VARCHAR(3), db.ForeignKey('instrument_type.code'), nullable=False)
    case_disposition_code                   = db.Column(db.VARCHAR(4), db.ForeignKey('case_disposition.code'), nullable=False)
    court                                   = db.Column(db.Integer, nullable=False)
    case_status_code                        = db.Column(db.VARCHAR(1), db.ForeignKey('case_status.code'), nullable=False)
    defendant_status_code                   = db.Column(db.VARCHAR(1), db.ForeignKey('defendant_status.code'), nullable=False)
    bond_amount                             = db.Column(db.Integer, nullable=True)
    current_offense_code                    = db.Column(db.Integer, nullable=False)
    current_offense_definition              = db.Column(db.VARCHAR(255), nullable=True)
    current_offense_level_degree_code       = db.Column(db.VARCHAR(2), db.ForeignKey('current_offense_level_degree.code'), nullable=False)
    next_appearance_date                    = db.Column(db.DateTime, nullable=True)
    docket_calendar_name_code               = db.Column(db.VARCHAR(3), db.ForeignKey('docket_calendar_name.code'), nullable=True)
    calendar_reason_code                    = db.Column(db.VARCHAR(4), db.ForeignKey('calendar_reason.code'), nullable=True)
    defendant_name                          = db.Column(db.VARCHAR(255), nullable=True)
    defendant_spn                           = db.Column(db.Integer, nullable=False)
    defendant_race_code                     = db.Column(db.VARCHAR(1), db.ForeignKey('defendant_race.code'), nullable=True)
    defendant_sex                           = db.Column(db.VARCHAR(1), nullable=True)
    defendant_date_of_birth                 = db.Column(db.DateTime, nullable=True)
    defendant_street_number                 = db.Column(db.VARCHAR(10), nullable=True)
    defendant_street_name                   = db.Column(db.VARCHAR(255), nullable=True)
    defendant_city                          = db.Column(db.VARCHAR(255), nullable=True)
    defendant_state                         = db.Column(db.VARCHAR(255), nullable=True)
    defendant_zip_code                      = db.Column(db.VARCHAR(10), nullable=True)
    attorney_name                           = db.Column(db.VARCHAR(255), nullable=True)
    attorney_spn                            = db.Column(db.Integer, nullable=True)
    attorney_connection_code                = db.Column(db.VARCHAR(3), nullable=True)
    attorney_connection_definition          = db.Column(db.VARCHAR(255), nullable=True)
    disposition_date                        = db.Column(db.DateTime, nullable=True)
    disposition                             = db.Column(db.VARCHAR(255), nullable=True)
    sentence                                = db.Column(db.VARCHAR(255), nullable=True)
    complainant_name                        = db.Column(db.VARCHAR(255), nullable=True)
    complainant_agency                      = db.Column(db.VARCHAR(255), nullable=True)
    offense_report_number                   = db.Column(db.VARCHAR(255), nullable=True)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
    