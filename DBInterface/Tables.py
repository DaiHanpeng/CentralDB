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


class SampleLocationTable(BaseModel):
    __tablename__ = 'sample_location'
    sid = Column(VARCHAR(24), primary_key=True, nullable=False,unique=True)
    location = Column(VARCHAR(24))
    timestamp = Column(DATETIME())

    def __init__(self,sid,location=None,timestamp=None):
        self.sid = sid
        self.location = location
        self.timestamp = timestamp

    def __repr__(self):
        return 'sample location information: \n'+\
               'sid:'+HORIZONTAL_TABLE+self.sid+\
               'location:'+HORIZONTAL_TABLE+self.location+\
               'update timestamp:'+HORIZONTAL_TABLE+self.timestamp


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
    flagged = Column(Integer())

    def __init__(self,\
                 test_name = None,\
                 dilution_profile = None,\
                 dilution_factor = None,\
                 result = None,\
                 datetime = None,\
                 instrument_id = None,\
                 sid = None,\
                 aspect = None,\
                 flagged = None):
        self.test_name = test_name
        self.dilution_factor = dilution_factor
        self.dilution_profile = dilution_profile
        self.result = result
        self.datetime = datetime
        self.instrument_id = instrument_id
        self.sid = sid
        self.aspect = aspect
        self.flagged = flagged

    def __repr__(self):
        return 'result information: \n'+\
               'test name:'+HORIZONTAL_TABLE+self.test_name+\
               'dilution profile:'+HORIZONTAL_TABLE+self.dilution_profile+\
               'dilution factor:'+HORIZONTAL_TABLE+self.dilution_factor+\
               'result:'+HORIZONTAL_TABLE+self.result+\
               'datetime:'+HORIZONTAL_TABLE+str(self.datetime)+\
               'instrument_id:'+HORIZONTAL_TABLE+str(self.instrument_id)+\
               'sid:'+HORIZONTAL_TABLE+self.sid,\
               'aspect:'+HORIZONTAL_TABLE+self.aspect,\
               'flagged:'+HORIZONTAL_TABLE+self.flagged


class ResultFlagTable(BaseModel):
    __tablename__ = 'flag'
    fid = Column(Integer(), primary_key=True, nullable=False,unique=True)
    code = Column(VARCHAR(24))
    rid = Column(Integer())

    def __init__(self,code=None,rid=None):
        self.code = code
        self.rid = rid

    def __repr__(self):
        return 'result flag information: \n'+\
               'fid:'+HORIZONTAL_TABLE+self.fid+\
               'flag code:'+HORIZONTAL_TABLE+self.code+\
               'rid:'+HORIZONTAL_TABLE+self.rid


class LasLogTable(BaseModel):
    __tablename__ = 'las_log'
    id = Column(Integer(),primary_key=True, nullable=False,autoincrement=True,unique=True)
    node_id = Column(VARCHAR(45))
    sample_id = Column(VARCHAR(45))
    carrier_id = Column(VARCHAR(45))
    timestamp = Column(DATETIME())
    node_type = Column(VARCHAR(45))
    log_code = Column(VARCHAR(45))
    need_deliver = Column(CHAR(1))
    delivered = Column(CHAR(1))
    delivered_time_stamp = Column(DATETIME())

    def __init__(self,\
                 node_id=None,\
                 sample_id=None, \
                 carrier_id=None, \
                 timestamp=None,\
                 node_type=None,\
                 log_code=None,\
                 need_deliver=None,\
                 delivered=None,\
                 delivered_time_stamp=None):
        self.node_id = node_id
        self.sample_id = sample_id
        self.carrier_id = carrier_id
        self.timestamp = timestamp
        self.node_type = node_type
        self.log_code = log_code
        self.need_deliver = need_deliver
        self.delivered = delivered
        self.delivered_time_stamp = delivered_time_stamp

    def __repr__(self):
        return 'las log: \n'+\
               'node_id:' + HORIZONTAL_TABLE+str(self.node_id) + ',' + \
               'sample_id:' + HORIZONTAL_TABLE+str(self.sample_id) + ',' + \
               'carrier_id:' + HORIZONTAL_TABLE + str(self.carrier_id) + ',' + \
               'timestamp:' + HORIZONTAL_TABLE + str(self.timestamp) + ',' + \
               'node_type:' + HORIZONTAL_TABLE + str(self.node_type) + ',' + \
               'log_code:' + HORIZONTAL_TABLE + str(self.log_code) + ',' + \
               'need_deliver:' + HORIZONTAL_TABLE + str(self.need_deliver) + ',' + \
               'delivered:' + HORIZONTAL_TABLE + str(self.delivered) + ',' + \
               'delivered_time_stamp:' + HORIZONTAL_TABLE + str(self.delivered_time_stamp)
