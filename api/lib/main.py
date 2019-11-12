from flask import request, Flask
import json  # python的轻量级的开发框架
from flask_sqlalchemy import SQLAlchemy  # 导入
from conf import config
from sqlalchemy.ext.declarative import declarative_base
from lib.tools import serialize, DecimalEncoder, convert_time
from lib.log import Log
from lib.common import get_hourly_chime
import datetime
import multiprocessing

# 接口，后台服务的开发
# 在浏览器运行http://127.0.0.1:8080/get_ms_info，或者其他访问接口的方式
# __name__当前文件名，把app python当做一个server
server = Flask(__name__)
server.config.from_object(config)
db = SQLAlchemy(server)
Base = declarative_base()
log = Log()


class TradeAdvice(db.Model):
    __tablename__ = 't_trade_advice'
    masaTransactionID = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    clientID = db.Column(db.INTEGER, nullable=True)
    clientReference = db.Column(db.String(64), nullable=True)
    clientOrderID = db.Column(db.String(64), nullable=True)
    masaAccountID = db.Column(db.String(64), nullable=True)
    masaSubAccountID = db.Column(db.String(64), nullable=True)
    masaPortfolioID = db.Column(db.String(64), nullable=True)
    masaReference = db.Column(db.String(64), nullable=True)
    externalReferenceID = db.Column(db.String(64), nullable=True)
    buySell = db.Column(db.INTEGER, nullable=True)
    orderQuantity = db.Column(db.DECIMAL(10, 4), nullable=True)
    instrumentID = db.Column(db.String(64), nullable=True)
    instrumentCurrency = db.Column(db.String(64), nullable=True)
    orderType = db.Column(db.String(64), nullable=True)
    orderTimeInForce = db.Column(db.String(64), nullable=True)
    orderCleanPrice = db.Column(db.DECIMAL(10, 4), nullable=True)
    orderInstructions = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradeQuantity = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradeCleanPrice = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradedCleanValue = db.Column(db.DECIMAL(10, 4), nullable=True)
    accruedInterest = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradedDirtyValue = db.Column(db.DECIMAL(10, 4), nullable=True)
    transactionFees = db.Column(db.DECIMAL(10, 4), nullable=True)
    settlementAmount = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradeDate = db.Column(db.DATETIME, nullable=True)
    settlementDate = db.Column(db.DATETIME, nullable=True)
    settlementCurrency = db.Column(db.String(64), nullable=True)
    status = db.Column(db.INTEGER, nullable=True)
    statusMessage = db.Column(db.String(64), nullable=True)
    xRecTimestamp = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '"ms订单号:%r"' % self.masaTransactionID


class InstrumentQuotes(db.Model):
    __tablename__ = 't_instrument_quotes'
    instrumentID = db.Column(db.String(32), primary_key=True)
    description = db.Column(db.String(64), nullable=True)
    issuer = db.Column(db.String(64), nullable=True)
    currency = db.Column(db.String(32), nullable=True)
    couponType = db.Column(db.String(32), nullable=True)
    currentCoupon = db.Column(db.DECIMAL(10, 4), nullable=True)
    couponFreq = db.Column(db.INTEGER, nullable=True)
    nextCallDate = db.Column(db.DATETIME, nullable=True)
    nextCouponDate = db.Column(db.DATETIME, nullable=True)
    businessDaysToSettle = db.Column(db.INTEGER, nullable=True)
    settlementDate = db.Column(db.DATETIME, nullable=True)
    grossAmount = db.Column(db.DECIMAL(10, 4), nullable=True)
    accruedInterest = db.Column(db.DECIMAL(10, 6), nullable=True)
    daysAccrued = db.Column(db.INTEGER, nullable=True)
    totalAmount = db.Column(db.DECIMAL(10, 4), nullable=True)
    msBidPrice = db.Column(db.DECIMAL(10, 4), nullable=True)
    msOfferPrice = db.Column(db.DECIMAL(10, 4), nullable=True)
    msBidYield = db.Column(db.DECIMAL(10, 4), nullable=True)
    msOfferYield = db.Column(db.DECIMAL(10, 4), nullable=True)
    notionalQuantity = db.Column(db.DECIMAL(10, 4), nullable=True)
    tradeDate = db.Column(db.DATETIME, nullable=True)
    quoteId = db.Column(db.String(64), nullable=True)
    xRecTimestamp = db.Column(db.String(64), nullable=True)


db.create_all()


@server.route('/')
def hello_world():
    return 'APP START!'


@server.route('/api/BondOrder', methods=['get', 'post', 'delete'])
def bond_order():
    if request.method == 'GET':
        try:
            log.info("get参数:%s" % request.args)
            masa_transaction_id = request.args.get('MasaTransactionID')
            log.info("查询订单ID:%s" % masa_transaction_id)
            get_result = TradeAdvice.query.filter(TradeAdvice.masaTransactionID == masa_transaction_id).first()
            if get_result is None:
                return json.loads('{"error":"没有该商户订单对应的MS订单"}')
            else:
                get_result_dict = serialize(get_result)
                get_order_info = json.dumps(get_result_dict, cls=DecimalEncoder)
                return json.loads(get_order_info)
        except Exception as e:
            log.error(e)
            return json.loads('{"error":"没有该商户订单对应的MS订单"}')
    elif request.method == 'POST':
        try:
            create_order_data = eval(request.data)
            log.info("创建订单请求参数:%s" % create_order_data)
            client_order_id = create_order_data['clientOrderID']
            get_result = TradeAdvice.query.filter(TradeAdvice.clientOrderID == client_order_id).first()
            if get_result is None:
                create_order_data['status'] = 9
                create_order_data['masaAccountID'] = 'MS1003341'
                create_order_data['masaSubAccountID'] = 'MS1003341-001'
                create_order_data['masaPortfolioID'] = 'Standard SDA SELF-DIRECTED'
                create_order_data['tradeDate'] = datetime.datetime.now()
                trade_advice = TradeAdvice(**create_order_data)
                db.session.add(trade_advice)
                db.session.commit()
                create_result = TradeAdvice.query.filter(TradeAdvice.clientOrderID == client_order_id).first()
                create_result_dict = serialize(create_result)
                create_order_info = json.dumps(create_result_dict, cls=DecimalEncoder)
                log.info("创建订单返回参数: %s" % json.loads(create_order_info))
                return json.loads(create_order_info)
            else:
                get_result_dict = serialize(get_result)
                get_order_info = json.dumps(get_result_dict, cls=DecimalEncoder)
                log.info("创建订单返回参数: %s" % json.loads(get_order_info))
                return json.loads(get_order_info)
        except Exception as e:
            log.error(e)
            return json.loads('{"error":"服务器错误"}')
    # elif request.method == 'DELETE':
    #     client_order_id = request.args.get('clientOrderID')
    #     order_delete = TradeAdvice.query.filter(TradeAdvice.clientOrderID == client_order_id).first()
    #     db.session.delete(order_delete)
    #     db.session.commit()
    else:
        """取消"""
        pass


@server.route('/api/Access/GetAuthToken', methods=['get', 'post'])
def get_auth_token():
    return "token check success"


@server.route('/api/Access/Login', methods=['get', 'post'])
def login():
    return "login success"


@server.route('/api/InstrumentQuote3/GetAllInstrumentQuotes3')
def get_all_instrument_quotes():
    """MS债券行情mock"""
    list = []
    get_results = InstrumentQuotes.query.all()
    for get_result in get_results:
        get_result_dict = serialize(get_result)
        get_result_dict['tradeDate'] = convert_time(get_hourly_chime(datetime.datetime.now()))
        get_result_dict['settlementDate'] = convert_time(
            get_hourly_chime(datetime.datetime.now() + datetime.timedelta(days=2)))
        get_order_info = json.dumps(get_result_dict, cls=DecimalEncoder)
        list.append(json.loads(get_order_info))
    log.info('MS行情:%s' % list)
    return str(list)


status = {"received": 1,
          "verified": 2,
          "traded": 3,
          "complete": 4,
          "cancelled": 5,
          "MasaAPI verification failed": 6,
          "OMS verification failed": 7,
          "Sent to OMS": 8,
          "process": 9}


@server.route('/api/set_trade_value', methods=['get', 'post'])
def set_trade_value():
    """模拟MS返回值"""
    try:
        get_results = TradeAdvice.query.filter(TradeAdvice.status != 4).all()
        for get_result in get_results:
            get_result_dict = serialize(get_result)
            get_result.tradeQuantity = get_result_dict['orderQuantity']
            get_result.tradeCleanPrice = 103
            get_result.tradedCleanValue = 1.03 * float(get_result_dict['orderQuantity'])
            get_result.accruedInterest = 0.04 * float(get_result_dict['orderQuantity'])
            get_result.transactionFees = 31.36
            get_result.tradedDirtyValue = float(get_result.tradedCleanValue) + float(
                get_result.accruedInterest) + float(get_result.transactionFees)
            get_result.status = 4
            # get_result.settlementDate = datetime.datetime.now() + datetime.timedelta(days=2)
            get_result.settlementDate = datetime.datetime.now()
            db.session.commit()
        return "set data success"
    except Exception as e:
        log.error(e)
        return "set data fail"


from lib.timer import set_data_timer

t = multiprocessing.Process(target=set_data_timer)
t.start()
