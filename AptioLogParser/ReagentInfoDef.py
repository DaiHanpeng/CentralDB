
HORIZONTAL_TABLE = b'\x09'

class ReagentInfoItem():
    '''
    This class if defined for a single reagent info unit, from the table's view, its a cell of the table.
    '''
    def __init__(self, reagent_name, reagent_count):
        self.reagent_name = reagent_name
        self.reagent_count = reagent_count

    def __repr__(self):
        return 'reagent name: ' + self.reagent_name + HORIZONTAL_TABLE +\
               'reagent count: ' + str(self.reagent_count)


class InstrumentReagentInfo():
    '''
    This class is defined for single instrument,from the table's view, its a column of the reagent info table.
    '''
    def __init__(self, instr_id, instr_type, time_stamp=None, reagent_info_list=[]):
        '''
        Instrument_Id: str
        Instrument_Type: str
        Reagent_Info_List: ReagentInfoItem[]
        '''
        self.instrument_id = instr_id
        self.instrument_type = instr_type
        self.time_stamp = time_stamp
        self.reagent_info_list = reagent_info_list

    def __repr__(self):
        return 'instrument id: '+ self.instrument_id + HORIZONTAL_TABLE +\
                'instrument type: ' + self.instrument_type + HORIZONTAL_TABLE+\
                'updated timestamp: ' + str(self.time_stamp) + HORIZONTAL_TABLE+\
                '\nreagent inventory info:\n' + '\n'.join(str(item) for item in self.reagent_info_list)


class SystemReagentInfo():
    '''
    Reagent information of the whole system
    '''
    def __init__(self):
        self.system_reagent = []

    def update_instrument_reagent_inventory(self,instrument_reagent_invemtory):
        if isinstance(instrument_reagent_invemtory,InstrumentReagentInfo):
            if not self.get_last_update_timestamp_per_instrument(instrument_reagent_invemtory.instrument_id) or \
                    self.get_last_update_timestamp_per_instrument(instrument_reagent_invemtory.instrument_id)<instrument_reagent_invemtory.time_stamp:
                old_record = self.get_instrument_reagent_inventory_item_by_id(instrument_reagent_invemtory.instrument_id)
                if old_record:
                    old_record = instrument_reagent_invemtory
                else:
                    self.system_reagent.append(instrument_reagent_invemtory)

    def get_instrument_reagent_inventory_item_by_id(self,instr_id):
        for item in self.system_reagent:
            if isinstance(item,InstrumentReagentInfo):
                if item.instrument_id == instr_id:
                    return item

    def get_last_update_timestamp_per_instrument(self,instr_id):
        for item in self.system_reagent:
            if isinstance(item,InstrumentReagentInfo):
                if item.instrument_id == instr_id:
                    return item.time_stamp

    def __repr__(self):
        return 'system reagent info:\n' +'\n'.join(str(item) for item in self.system_reagent)


def test01():
    ReagentInfoItem11 = ReagentInfoItem('dai', 12)
    ReagentInfoItem12 = ReagentInfoItem('han', 13)
    ReagentInfoItem13 = ReagentInfoItem('peng', 14)
    ReagentInfoList1 = [ReagentInfoItem11, ReagentInfoItem12, ReagentInfoItem13]

    ReagentInfoItem21 = ReagentInfoItem('I', 32)
    ReagentInfoItem22 = ReagentInfoItem('love', 33)
    ReagentInfoItem23 = ReagentInfoItem('python', 34)
    ReagentInfoList2 = [ReagentInfoItem21, ReagentInfoItem22, ReagentInfoItem23]

    # 'normal testing, below info should be updated:'
    InstrumentInfo1 = InstrumentReagentInfo('5', 'A24', '20160101110909', ReagentInfoList1)
    InstrumentInfo2 = InstrumentReagentInfo('7', 'CEN', '20151212090923', ReagentInfoList2)
    # 'abnormal testing, below info should not be updated:'
    InstrumentInfo3 = InstrumentReagentInfo('5', 'A24', '20150101110909', ReagentInfoList2)

    aptioReagentInfo = SystemReagentInfo()

    aptioReagentInfo.update_instrument_reagent_inventory(InstrumentInfo1)
    aptioReagentInfo.update_instrument_reagent_inventory(InstrumentInfo2)

    aptioReagentInfo.update_instrument_reagent_inventory(InstrumentInfo3)

    print aptioReagentInfo

def test02():
    from datetime import datetime
    dt1 = '20141117100340'
    dt = datetime.strptime(dt1,'%Y%m%d%H%M%S')
    print dt < None

if __name__ == '__main__':
    test02()