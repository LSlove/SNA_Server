# -*- coding: utf-8 -*-

import sys
from pysnmp import hlapi
import traceback

#snmp정보
class SnaSnmp(object):
    def __init__(self):#최초시작
        self.COUNTER64_MAX_VALUE = 18446744073709551615 #64비트 최댓값
        self.COUNTER32_MAX_VALUE = 4294967295 #32비트 최댓값

    def _construct_object_types(self, list_of_oids): #oid 실제 구별할 값 찾기
        object_types = []
        for oid in list_of_oids:
            try : 
                object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
            except Exception as e:
                print('> _construct_object_types : ', e)
                traceback.print_exc(file=sys.stdout)
                continue

        return object_types

    def _construct_value_pairs(self, list_of_pairs):#
        pairs = []
        for key, value in list_of_pairs.items():
            pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
        return pairs

    def _fetch(self, handler, count):#
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = self._cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
            except RuntimeError:
                print('>> Got SNMP error: {0}-{1}'.format(error_indication, error_status))
                return -1
        return result

    def _cast(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    #snmp 데이터 가져오기
    def get(self, target, oids, community, port=161, version=1, timeout=1, retries=3, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        try :
            handler = hlapi.getCmd(
                engine,
                hlapi.CommunityData(community, mpModel=version),
                hlapi.UdpTransportTarget((target, port), timeout=timeout, retries=retries),
                context,
                *self._construct_object_types(oids)
            )
        except Exception as e:
            print('> get : ', e)
            traceback.print_exc(file=sys.stdout)
            return -1

        fetch_value = self._fetch(handler, 1)

        if fetch_value != -1:
            return fetch_value[0]
        else:
            return fetch_value

    #
    def get_bulk(self, target, oids, community, count, version=1, timeout=1, retries=3, start_from=0, port=161,
                engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        try :
            handler = hlapi.bulkCmd(
                engine,
                hlapi.CommunityData(community, mpModel=version),
                hlapi.UdpTransportTarget((target, port), timeout=timeout, retries=retries),
                context,
                start_from, count,
                *self._construct_object_types(oids)
            )
        except Exception as e:
            print('> get_bulk : ', e)
            traceback.print_exc(file=sys.stdout)
            return None

        return self._fetch(handler, count)


    def get_bulk_auto(self, target, oids, community, count_oid, version=1, timeout=1, retries=3, 
                start_from=0, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        count = self.get(target, [count_oid], community, port, version, timeout, retries, engine, context)
        if count == -1 :
            return None
        else:
            return self.get_bulk(target, oids, community, count[count_oid], version, 
                            timeout, retries, start_from, port, engine, context)


    def set(self, target, value_pairs, community, port=161, version=1, timeout=1, retries=3,
            engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        try :
            handler = hlapi.setCmd(
                engine,
                hlapi.CommunityData(community, mpModel=version),
                hlapi.UdpTransportTarget((target, port), timeout=timeout, retries=retries),
                context,
                *self._construct_value_pairs(value_pairs)
            )
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return -1

        fetch_value = self._fetch(handler, 1)

        if fetch_value != -1:
            return fetch_value[0]
        else:
            return fetch_value


    def calc_counter32(self, prev_value, curr_value):
        real_value = 0
        if curr_value >= prev_value:
            real_value = curr_value - prev_value
        else:
            real_value = (self.COUNTER32_MAX_VALUE - prev_value) + curr_value

        return real_value


    def calc_counter64(self, prev_value, curr_value):
        real_value = 0
        if curr_value >= prev_value:
            real_value = curr_value - prev_value
        else:
            real_value = (self.COUNTER64_MAX_VALUE - prev_value) + curr_value

        return real_value