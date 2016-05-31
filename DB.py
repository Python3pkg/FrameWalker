from peewee import *
'''
Setup:

    Python:
    pip install peewee
    pip install PyMySQL

    DB:
    Install MySQL
    Install MySQL Workbench
    Add new schema "frameway"
    In %PROGRAMDATA%\MySQL\MySQL Server X.x\my.ini, remove STRICT_TRANS_TABLES and restart MySQL servcie
    Create view 'all':
        CREATE
            ALGORITHM = UNDEFINED
            DEFINER = `root`@`localhost`
            SQL SECURITY DEFINER
        VIEW `all` AS
            SELECT
                `testcase`.`test_case_timestamp` AS `test_case_timestamp`,
                `testcase`.`test_case_comment` AS `test_case_comment`,
                `transaction`.`transaction_timestamp` AS `transaction_timestamp`,
                `transaction`.`transaction_name` AS `transaction_name`,
                `transaction`.`transaction_iteration` AS `transaction_iteration`,
                `transaction`.`transaction_time` AS `transaction_time`,
                `frame`.`frame_attributes` AS `frame_attributes`,
                `frame`.`frame_hashed_src` AS `frame_hashed_src`,
                `frame`.`frame_src` AS `frame_src`,
                `frame`.`frame_relative_start_time` AS `frame_relative_start_time`,
                `frame`.`frame_time` AS `frame_time`,
                `frame`.`frame_resources_relative_start_time` AS `frame_resources_relative_start_time`,
                `frame`.`frame_resources_time` AS `frame_resources_time`,
                NULL AS `resource_name`,
                NULL AS `resource_time`,
                NULL AS `resource_relative_start_time`,
                `timing`.`timing_time` AS `timing_time`,
                `timing`.`timing_relative_start_time` AS `timing_relative_start_time`
            FROM
                (((`testcase`
                JOIN `transaction` ON ((`testcase`.`test_case_id` = `transaction`.`test_case_id`)))
                JOIN `frame` ON ((`transaction`.`transaction_id` = `frame`.`transaction_id`)))
                JOIN `timing` ON ((`frame`.`frame_id` = `timing`.`frame_id`)))
            WHERE
                (`testcase`.`test_case_id` > 0)
            UNION SELECT
                `testcase`.`test_case_timestamp` AS `test_case_timestamp`,
                `testcase`.`test_case_comment` AS `test_case_comment`,
                `transaction`.`transaction_timestamp` AS `transaction_timestamp`,
                `transaction`.`transaction_name` AS `transaction_name`,
                `transaction`.`transaction_iteration` AS `transaction_iteration`,
                `transaction`.`transaction_time` AS `transaction_time`,
                `frame`.`frame_attributes` AS `frame_attributes`,
                `frame`.`frame_hashed_src` AS `frame_hashed_src`,
                `frame`.`frame_src` AS `frame_src`,
                `frame`.`frame_relative_start_time` AS `frame_relative_start_time`,
                `frame`.`frame_time` AS `frame_time`,
                `frame`.`frame_resources_relative_start_time` AS `frame_resources_relative_start_time`,
                `frame`.`frame_resources_time` AS `frame_resources_time`,
                `resource`.`resource_name` AS `resource_name`,
                `resource`.`resource_time` AS `resource_time`,
                `resource`.`resource_relative_start_time` AS `resource_relative_start_time`,
                NULL AS `timing_time`,
                NULL AS `timing_relative_start_time`
            FROM
                (((`testcase`
                JOIN `transaction` ON ((`testcase`.`test_case_id` = `transaction`.`test_case_id`)))
                JOIN `frame` ON ((`transaction`.`transaction_id` = `frame`.`transaction_id`)))
                JOIN `resource` ON ((`frame`.`frame_id` = `resource`.`frame_id`)))
            WHERE
                (`testcase`.`test_case_id` > 0)

Other:

    Drop all tables:
    DROP TABLE `frameway`.`resource`;
    DROP TABLE `frameway`.`timing`;
    DROP TABLE `frameway`.`frame`;
    DROP TABLE `frameway`.`transaction`;
    DROP TABLE `frameway`.`testcase`
'''

timeStampFormat = '%Y-%m-%d %H:%M:%S.%f'
DB = MySQLDatabase("frameway", host="127.0.0.1", port=3306, user="dbuser", password="dbuser")
# Jens was here
class BaseModel(Model):
    class Meta:
        database = DB


class TestCase(BaseModel):
    test_case_id = PrimaryKeyField()
    test_case_timestamp = DateTimeField(timeStampFormat)
    test_case_comment = TextField()


class Transaction(BaseModel):
    transaction_id = PrimaryKeyField()
    test_case = ForeignKeyField(TestCase, related_name='transaction')
    transaction_name = CharField()
    transaction_timestamp = DateTimeField(timeStampFormat)
    transaction_iteration = IntegerField()
    transaction_start_time = DoubleField(default=-1)
    transaction_time = IntegerField(default=-1)


class Frame(BaseModel):
    frame_id = PrimaryKeyField()
    transaction = ForeignKeyField(Transaction, related_name='frame')
    frame_structure_id = CharField()
    frame_src = TextField()
    frame_hashed_src = CharField()
    frame_attributes = TextField()
    frame_relative_start_time = IntegerField(default=-1)
    frame_time = IntegerField(default=-1)
    frame_resources_relative_start_time = IntegerField(default=-1)
    frame_resources_time = IntegerField(default=-1)


class Timing(BaseModel):
    timing_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='timing')
    navigationStart = DoubleField()
    redirectStart = DoubleField()
    redirectEnd = DoubleField()
    fetchStart = DoubleField()
    domainLookupStart = DoubleField()
    domainLookupEnd = DoubleField()
    connectStart = DoubleField()
    secureConnectionStart = DoubleField()
    connectEnd = DoubleField()
    requestStart = DoubleField()
    responseStart = DoubleField()
    responseEnd = DoubleField()
    domLoading = DoubleField()
    domInteractive = DoubleField()
    domContentLoadedEventStart = DoubleField()
    domContentLoadedEventEnd = DoubleField()
    domComplete = DoubleField()
    loadEventStart = DoubleField()
    loadEventEnd = DoubleField()
    unloadEventEnd = DoubleField()
    unloadEventStart = DoubleField()
    timing_redirect = IntegerField()
    timing_appcache = IntegerField()
    timing_dns = IntegerField()
    timing_dnstcp = IntegerField()
    timing_tcp = IntegerField()
    timing_blocked = IntegerField()
    timing_request = IntegerField()
    timing_dom = IntegerField()
    timing_onload = IntegerField()
    timing_relative_start_time = IntegerField(default=-1)
    timing_time = IntegerField(default=-1)


class Resource(BaseModel):
    resource_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='resource')
    resource_name = TextField()
    resource_start_time = IntegerField()
    resource_absolute_start_time = DoubleField(default=-1)
    resource_absolute_end_time = DoubleField(default=-1)
    resource_relative_start_time = IntegerField(default=-1)
    resource_time = IntegerField(default=-1)


def insertTestCase(timeStamp, comment):
    return TestCase.create(test_case_timestamp=timeStamp, test_case_comment=comment)


def insertTransaction(testCaseID, timeStamp, transactionName, iteration):
    return Transaction.create(test_case=testCaseID,
                              transaction_timestamp=timeStamp,
                              transaction_name=transactionName,
                              transaction_iteration=iteration)


def insertFrame(transactionID, frameStructureId, src, hashedSrc, attributes):
    return Frame.create(transaction=transactionID,
                        frame_structure_id=frameStructureId,
                        frame_src=src,
                        frame_hashed_src=hashedSrc,
                        frame_attributes=attributes)


def insertTiming(frameID, timing):
    timing["frame"] = frameID
    return Timing.insert(timing).execute()


def insertRecources(frameID, recourse):
    if len(recourse) > 0:
        for item in recourse:
            item.update({"frame": frameID})
        with DB.atomic():
            return Resource.insert_many(recourse).execute()
    return None


def addTransactionTimes(transaction):
    # Add transaction_start_time
    timingStartTimes = Timing\
        .select(Timing.navigationStart.alias('starttime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    resourceStartTimes = Resource\
        .select(Resource.resource_absolute_start_time.alias('starttime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
    Transaction\
        .update(transaction_start_time=startTime)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .execute()
    # Add transaction_time
    timingEndTimes = Timing\
        .select(Timing.loadEventEnd.alias('endtime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    resourceEndTimes = Resource\
        .select(Resource.resource_absolute_end_time.alias('endtime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
    Transaction\
        .update(transaction_time=endTime - startTime)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .execute()


def addFrameTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    frames = Frame.select().where(Frame.transaction == transaction.transaction_id).execute()
    for frame in frames:
        # Add frame_relative_start_time
        timingStartTimes = Timing\
            .select(Timing.navigationStart.alias('starttime'))\
            .where(Timing.frame == frame.frame_id)
        resourceStartTimes = Resource\
            .select(Resource.resource_absolute_start_time.alias('starttime'))\
            .where(Resource.frame == frame.frame_id)
        startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
        Frame\
            .update(frame_relative_start_time=startTime-transactionStartTime)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()
        # Add frame_time
        timingEndTimes = Timing\
            .select(Timing.loadEventEnd.alias('endtime'))\
            .where(Timing.frame == frame.frame_id)
        resourceEndTimes = Resource\
            .select(Resource.resource_absolute_end_time.alias('endtime'))\
            .where(Resource.frame == frame.frame_id)
        endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
        Frame\
            .update(frame_time=endTime - startTime)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()


def addTimingTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    query = 'update timing ' \
            'join frame ' \
            'on frame.frame_id = timing.frame_id ' \
            'set timing_relative_start_time = timing.navigationStart - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)


def addResourceTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    # Add resource_relative_start_time
    query = 'update resource ' \
            'join frame ' \
            'on frame.frame_id = resource.frame_id ' \
            'set resource_relative_start_time = resource.resource_absolute_start_time - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)
    # Add total resource times to frames
    frames = Frame\
        .select()\
        .where(Frame.transaction == transaction.transaction_id)\
        .execute()
    for frame in frames:
        # Add resources_relative_start_time
        try:
            resources_relative_start_time = Resource\
                .select(Resource.resource_relative_start_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(+Resource.resource_relative_start_time)\
                .get().resource_relative_start_time
        except DoesNotExist:
            resources_relative_start_time = -1
        Frame\
            .update(frame_resources_relative_start_time=resources_relative_start_time)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()
        # Add resources_time
        try:
            absolute_start_time = Resource\
                .select(Resource.resource_absolute_start_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(+Resource.resource_relative_start_time)\
                .get().resource_absolute_start_time
            absolute_end_time = Resource\
                .select(Resource.resource_absolute_end_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(-Resource.resource_absolute_end_time)\
                .get().resource_absolute_end_time
        except DoesNotExist:
            absolute_end_time = -1
            absolute_start_time = 0
        totalResourcesTime = absolute_end_time - absolute_start_time
        Frame\
            .update(frame_resources_time=totalResourcesTime)\
            .where(Frame.frame_id == frame.frame_id).execute()


def TransactionStartTime(transaction):
    return Transaction\
        .select(Transaction.transaction_start_time)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .get().transaction_start_time


def deleteTestRun(testCaseId):
    deleteResources(testCaseId)
    deleteTimings(testCaseId)
    deleteFrames(testCaseId)
    deleteTransactions(testCaseId)
    deleteTestCase(testCaseId)


def deleteTimings(testCaseId):
    query = 'delete t ' \
            'from timing t ' \
            'inner join frame f ' \
            'on t.frame_id = f.frame_id ' \
            'inner join transaction tr ' \
            'on f.transaction_id = tr.transaction_id ' \
            'and tr.test_case_id=%s' \
            % testCaseId
    DB.execute_sql(query)


def deleteResources(testCaseId):
    query = 'delete r ' \
            'from resource r ' \
            'inner join frame f ' \
            'on r.frame_id = f.frame_id ' \
            'inner join transaction tr ' \
            'on f.transaction_id = tr.transaction_id ' \
            'and tr.test_case_id=%s' \
            % testCaseId
    DB.execute_sql(query)


def deleteFrames(testCaseId):
    query = 'delete f ' \
            'from frame f ' \
            'inner join transaction tr ' \
            'on f.transaction_id = tr.transaction_id ' \
            'and tr.test_case_id=%s' \
            % testCaseId
    DB.execute_sql(query)


def deleteTransactions(testCaseId):
    query = 'delete tr ' \
            'from transaction tr ' \
            'where tr.test_case_id=%s' \
            % testCaseId
    DB.execute_sql(query)


def deleteTestCase(testCaseId):
    query = 'SET FOREIGN_KEY_CHECKS=0; ' \
            'delete ' \
            'from testcase ' \
            'where test_case_id=%s; ' \
            'SET FOREIGN_KEY_CHECKS=1' \
            % testCaseId
    DB.execute_sql(query)


def testCases():
    return TestCase.select().execute()


def transactionCount(testCaseId):
    return Transaction.select().where(Transaction.test_case == testCaseId).count()


def frameAlreadyExist(testCase, iteration, timing):
    return Timing.select()\
               .join(Frame)\
               .join(Transaction)\
               .join(TestCase)\
               .where((Timing.navigationStart == timing.get('navigationStart'))
                      & (Transaction.transaction_iteration == iteration)
                      & (TestCase.test_case_id == testCase.test_case_id))\
               .execute().count > 0


def transactionHasFrames(transaction):
    return Frame.select().where(Frame.transaction == transaction.transaction_id).execute().count > 0


def init():
    DB.connect()
    if not TestCase.table_exists():
        addTables()


def reconnect():
    destroy()
    init()


def addTables():
    DB.create_tables([TestCase, Transaction, Frame, Resource, Timing])


def destroy():
    DB.close()