import os
import json
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()
        
    
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()

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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()
    
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()
    
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()
    
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()

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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()

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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()
    
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
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()

class DefendantBirthplace(BaseDB):
    
    # tablename
    __tablename__ = 'defendant_birthplace'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(2), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()

class DefendantUSCitizen(BaseDB):
    
    # tablename
    __tablename__ = 'defendant_uscitizen'
    
    # table columns
    code                                    = db.Column(db.VARCHAR(1), unique=True, nullable=False)
    definition                              = db.Column(db.VARCHAR(255), nullable=False)
    
    # relationships
    
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
    
    @classmethod
    def seed_db(cls, data_path):
        data_filename = 'hcdc_%s.json'%(cls.__tablename__)
        data_filepath = os.path.join(data_path, data_filename)
        
         # open data file
        try: 
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise
        
        for d in data:
            # create instance of class
            new_instance = cls()
            new_instance.code = d['code']
            new_instance.definition = d['definition']
            
            # add the new instance of the class to the db session
            db.session.add(new_instance)
        
        # save database session to the database
        db.session.commit()