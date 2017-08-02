# -*- coding: utf-8 -*-

from ml.preprocess.mining import mining

class baoer(mining):

    bkj_id = 0

    def find_serially(self,data_flow):

        # if data_flow.key == 'bkj_id' and 'bkj_id' in data_flow.a_n_minus_i :
        #     if len(data_flow.a_n_minus_i['bkj_id'])!=0:
        #         if int(data_flow.a_n_minus_i['bkj_id'][0]) - int(data_flow.value)==0:
        #             self.bkj_id +=1
        #         elif abs(int(data_flow.a_n_minus_i['bkj_id'][0]) - int(data_flow.value)) == 1:
        #             self.bkj_id +=2
        #         else: pass
        #         data_flow.value = self.bkj_id
        #     else:
        #         data_flow.value = 0
        #         self.bkj_id = 0
        return data_flow