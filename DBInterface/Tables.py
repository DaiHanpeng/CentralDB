from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String,DATETIME,TEXT,VARCHAR,DATE
from sqlalchemy.ext import declarative

HORIZONTAL_TABLE = b'\x09'


def TableArgsMeta(table_args):

    class _TableArgsMeta(declarative.DeclarativeMeta):

        def __init__(cls, name, bases, dict_):
            if (    # Do not extend base class
                    '_decl_class_registry' not in cls.__dict__ and
                    # Missing __tablename_ or equal to None means single table
                    # inheritance no table for it (columns go to table of
                    # base class)
                    cls.__dict__.get('__tablename__') and
                    # Abstract class no table for it (columns go to table[s]
                    # of subclass[es]
                    not cls.__dict__.get('__abstract__', False)):
                ta = getattr(cls, '__table_args__', {})
                if isinstance(ta, dict):
                    ta = dict(table_args, **ta)
                    cls.__table_args__ = ta
                else:
                    assert isinstance(ta, tuple)
                    if ta and isinstance(ta[-1], dict):
                        tad = dict(table_args, **ta[-1])
                        ta = ta[:-1]
                    else:
                        tad = dict(table_args)
                    cls.__table_args__ = ta + (tad,)
            super(_TableArgsMeta, cls).__init__(name, bases, dict_)

    return _TableArgsMeta


BaseModel = declarative_base(
            name='Base',
            metaclass=TableArgsMeta({'mysql_engine': 'InnoDB'}))



#BaseModel = declarative_base()


class LastUpdateTimestampTable(BaseModel):
    __tablename__ = 'last_update_timestamp'
    type_id = Column(VARCHAR(16), primary_key=True, nullable=False)
    last_file_update_timestamp = Column(DATETIME())
    last_record_update_timestamp = Column(DATETIME())

    def __init__(self,\
                 type_id,
                 last_file_update_timestamp=None,\
                 last_record_update_timestamp=None):
        self.type_id = type_id
        self.last_file_update_timestamp = last_file_update_timestamp
        self.last_record_update_timestamp = last_record_update_timestamp


class ReagentInventoryTable(BaseModel):
    __tablename__ = 'reagent_inventory'
    node_id = Column(VARCHAR(45),primary_key=True, nullable=False)
    node_type = Column(VARCHAR(45),primary_key=True, nullable=False)
    reagent_name = Column(VARCHAR(45),primary_key=True, nullable=False)
    reagent_type = Column(VARCHAR(45),primary_key=True, nullable=False)#reagent name can be All|Primary|Auxiliary
    reagent_count = Column(Integer())
    reagent_warn_threshold = Column(Integer())
    reagent_err_threshold = Column(Integer())
    expire_date_time = Column(DATETIME())
    reagent_pack_lot = Column(VARCHAR(45))
    updated_timestamp = Column(DATETIME())

    def __init__(self,\
                 node_id='NodeID',\
                 node_type='NodeType',\
                 reagent_name='ReagentName',\
                 reagent_type='All',\
                 reagent_count=None,\
                 reagent_warn_threshold=None,\
                 reagent_err_threshold=None,\
                 expire_date_time=None,\
                 reagent_pack_lot=None,\
                 updated_timestamp=None):
        self.id = id
        self.node_id = node_id
        self.node_type = node_type
        self.reagent_name = reagent_name
        self.reagent_type = reagent_type
        self.reagent_count = reagent_count
        self.reagent_warn_threshold = reagent_warn_threshold
        self.reagent_err_threshold = reagent_err_threshold
        self.expire_date_time = expire_date_time
        self.reagent_pack_lot = reagent_pack_lot
        self.updated_timestamp = updated_timestamp

class PatientTable(BaseModel):
    __tablename__ = 'patient'
    pid = Column(VARCHAR(24), primary_key=True, nullable=False,unique=True)
    fname = Column(VARCHAR(45))
    lname = Column(VARCHAR(45))
    birthday = Column(DATE())
    sex = Column(VARCHAR(45))
    location = Column(VARCHAR(45))

    def __init__(self,pid,\
                 fname=None,\
                 lname=None,\
                 birthday=None,\
                 sex=None,\
                 location=None):
        self.pid = pid
        self.fname = fname
        self.lname = lname
        self.birthday = birthday
        self.sex = sex
        self.location = location

    def __repr__(self):
        return 'patient information: \n'+\
               'pid:'+HORIZONTAL_TABLE+self.pid+\
               'fname:'+HORIZONTAL_TABLE+self.fname+\
               'lname:'+HORIZONTAL_TABLE+self.lname+\
               'birthday:'+HORIZONTAL_TABLE+str(self.birthday)+\
               'sex:'+HORIZONTAL_TABLE+self.sex+\
               'location:'+HORIZONTAL_TABLE+self.location

class SampleTable(BaseModel):
    __tablename__ = 'sample'
    sid = Column(VARCHAR(24), primary_key=True, nullable=False,unique=True)
    tube_type = Column(VARCHAR(45))
    sample_type = Column(VARCHAR(45))
    pid = Column(VARCHAR(24))

    def __init__(self,sid,tube_type=None,sample_type=None,pid=None):
        self.sid = sid
        self.tube_type = tube_type
        self.sample_type = sample_type
        self.pid = pid

    def __repr__(self):
        return 'sample information: \n'+\
               'sid:'+HORIZONTAL_TABLE+self.sid+\
               'tube type:'+HORIZONTAL_TABLE+self.tube_type+\
               'sample type:'+HORIZONTAL_TABLE+self.sample_type+\
               'pid:'+HORIZONTAL_TABLE+self.pid

class ResultTable(BaseModel):
    __tablename__ = 'result'
    rid = Column(Integer(), primary_key=True, nullable=False,unique=True)
    test_name = Column(VARCHAR(45))
    dilution_profile = Column(VARCHAR(45))
    dilution_factor = Column(VARCHAR(45))
    result = Column(VARCHAR(45))
    datetime = Column(DATETIME())
    instrument_id = Column(VARCHAR(45))
    sid = Column(VARCHAR(24))
    aspect = Column(VARCHAR(45))

    def __init__(self,\
                 test_name = None,\
                 dilution_profile = None,\
                 dilution_factor = None,\
                 result = None,\
                 datetime = None,\
                 instrument_id = None,\
                 sid = None,\
                 aspect = None):
        self.test_name = test_name
        self.dilution_factor = dilution_factor
        self.dilution_profile = dilution_profile
        self.result = result
        self.datetime = datetime
        self.instrument_id = instrument_id
        self.sid = sid
        self.aspect = aspect

    def __repr__(self):
        return 'result information: \n'+\
               'test name:'+HORIZONTAL_TABLE+self.test_name+\
               'dilution profile:'+HORIZONTAL_TABLE+self.dilution_profile+\
               'dilution factor:'+HORIZONTAL_TABLE+self.dilution_factor+\
               'result:'+HORIZONTAL_TABLE+self.result+\
               'datetime:'+HORIZONTAL_TABLE+str(self.datetime)+\
               'instrument_id:'+HORIZONTAL_TABLE+str(self.instrument_id)+\
               'sid:'+HORIZONTAL_TABLE+self.sid,\
               'aspecy:'+HORIZONTAL_TABLE+self.aspect
