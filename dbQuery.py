import sqlite3 as sql


def listComponents():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM componentTable")

            con.commit()
            response = cur.fetchall()
            msg = "done"
    except:
        con.rollback()
        msg = "fail"

    finally:
        return response
        con.close()


def addComponents(name, contact, manufacturer, fail_rate):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO componentTable(name, contact, manufacturer, fail_rate) VALUES(?, ?, ?, ?)",
                (name, contact, manufacturer, fail_rate))

            con.commit()
            msg = "done"
    except:
        con.rollback()
        msg = "fail"

    finally:
        con.close()


def removeComponent(id):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM componentTable WHERE num=" + id)
            cur.execute(
                "DELETE FROM mappingTable WHERE component_id=" + id)
            con.commit()
            msg = "delete done"
    except:
        con.rollback()
        msg = "delete fail"

    finally:
        return msg
        con.close()


def updateComponent(id, name, contact, manufacturer, fail_rate):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE componentTable SET name =?, contact=?, manufacturer=?, fail_rate=? WHERE num=?",
                (name, contact, manufacturer, fail_rate, id))
            cur.execute(
                "UPDATE mappingTable SET component =? WHERE component_id =?",
                (name, id))
            con.commit()
            msg = "update done"
    except:
        con.rollback()
        msg = "update fail"

    finally:
        return msg
        con.close()


def listFalmodes():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM failModesTable")

            con.commit()
            response = cur.fetchall()
            msg = "list fm done"
    except:
        con.rollback()
        msg = "list fm fail"

    finally:
        return response
        con.close()


def addFailMode(name, failmode_des):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO failModesTable(name, describe ) VALUES(?, ?)",
                        (name, failmode_des))
            con.commit()
            msg = "add fm done"
    except:
        con.rollback()
        msg = "add fm fail"

    finally:
        con.close()


def removeFailMode(id):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM failModesTable WHERE num=" + id)
            cur.execute(
                "DELETE FROM mappingTable WHERE fail_mode_id=" + id)
            con.commit()
            msg = "fm delete done"
    except:
        con.rollback()
        msg = "fm delete fail"

    finally:
        return msg
        con.close()


def updateFailMode(id, name, failmode_des):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE failModesTable SET name =?, describe=? WHERE num=?",
                (name, failmode_des, id))
            cur.execute(
                "UPDATE mappingTable SET fail_mode =? WHERE fail_mode_id=?",
                (name, id))
            con.commit()
            msg = "update done"
    except:
        con.rollback()
        msg = "update fail"

    finally:
        return msg
        con.close()

def listMappings():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM mappingTable")

            con.commit()
            response = cur.fetchall()
            msg = "done"
    except:
        con.rollback()
        msg = "fail"

    finally:
        return response
        con.close()


def getComponentById(cid):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM componentTable WHERE num=" + cid)
            component = cur.fetchone()
            component = component[1]
            con.commit()
    except:
        con.rollback()
        component = "fail"

    finally:
        con.close()
        return component


def getFailModeById(fid):
    try:
        with sql.connect("database.db") as con2:
            cur2 = con2.cursor()
            cur2.execute("SELECT * FROM failModesTable WHERE num=" + fid)
            fail_mode = cur2.fetchone()
            fail_mode = fail_mode[1]
            con2.commit()
    except:
        con2.rollback()
        fail_mode = "fm_fail"

    finally:
        con2.close()
        return fail_mode


def addMapping(fail_code, component_id, fail_mode_id):
    component = getComponentById(component_id)
    failmode = getFailModeById(fail_mode_id)
    try:
        with sql.connect("database.db") as con3:
            print(fail_code, component, failmode, component_id, fail_mode_id, '#####')
            cur = con3.cursor()
            cur.execute(
                "INSERT INTO mappingTable(fail_code, component, fail_mode, "
                "component_id, fail_mode_id) VALUES(?, ?, ?, ?, ?)",
                (fail_code, component, failmode, component_id, fail_mode_id))

            con3.commit()
            msg = "add mapping done"
    except:
        con3.rollback()
        msg = "add mapping fail"

    finally:
        con3.close()


def removeMapping(id):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM mappingTable WHERE num=" + id)

            con.commit()
            msg = "fm delete done"
    except:
        con.rollback()
        msg = "fm delete fail"

    finally:
        return msg
        con.close()


def updateMapping(id, fail_code, component_id, fail_mode_id):
    component = getComponentById(component_id)
    failmode = getFailModeById(fail_mode_id)
    try:
        with sql.connect("database.db") as con3:
            print(fail_code, component, failmode, component_id, fail_mode_id, '#####')
            cur = con3.cursor()
            cur.execute(
                "UPDATE mappingTable SET fail_code=?, component=?, fail_mode=?, component_id=?, fail_mode_id=? WHERE num=?",
                (fail_code, component, failmode, component_id, fail_mode_id, id))
            con3.commit()
            msg = "update mapping done"
    except:
        con3.rollback()
        msg = "update mapping fail"

    finally:
        con3.close()


def bad_components():
    try:
        with sql.connect("database.db") as con3:
            cur = con3.cursor()
            cur.execute(
                "SELECT name, fail_rate FROM componentTable ORDER BY fail_rate DESC")

            con3.commit()
            response = cur.fetchmany(5)
            msg = "done"
    except:
        con3.rollback()
        msg = "fail"

    finally:
        return response
        con3.close()


def mostUsed():
    try:
        with sql.connect("database.db") as con3:
            cur = con3.cursor()
            cur.execute("SELECT component, fail_rate FROM mappingTable LEFT JOIN componentTable"
                        " ON mappingTable.component_id = componentTable.num GROUP BY component "
                        "ORDER BY COUNT(component) DESC")

            con3.commit()
            response = cur.fetchmany(5)

            msg = "done"
    except:
        con3.rollback()
        msg = "fail"

    finally:
        return response
        con3.close()


def pfr():
    try:
        with sql.connect("database.db") as con3:
            cur = con3.cursor()
            cur.execute("SELECT manufacturer, ROUND(AVG(fail_rate), 2) FROM componentTable "
                        "GROUP BY manufacturer ORDER BY AVG(fail_rate) DESC")

            con3.commit()
            response = cur.fetchmany(3)

            msg = "done"
    except:
        con3.rollback()
        msg = "fail"

    finally:
        return response
        con3.close()


def ad():
    try:
        with sql.connect("database.db") as con3:
            cur = con3.cursor()
            cur.execute("SELECT manufacturer, ROUND(AVG(fail_rate), 2) FROM componentTable "
                        "GROUP BY manufacturer ORDER BY AVG(fail_rate) DESC")

            con3.commit()
            response_1 = cur.fetchmany(1)

            cur.execute("SELECT component, fail_rate FROM mappingTable LEFT JOIN componentTable"
                        " ON mappingTable.component_id = componentTable.num GROUP BY component "
                        "ORDER BY COUNT(component) DESC")

            con3.commit()
            response_2 = cur.fetchmany(1)

            cur.execute(
                "SELECT name, fail_rate, manufacturer, contact FROM componentTable ORDER BY fail_rate DESC")

            con3.commit()
            response_3 = cur.fetchmany(1)

            msg = "done"
    except:
        con3.rollback()
        msg = "fail"

    finally:
        return response_1 + response_2 + response_3
        con3.close()


def email():
    try:
        with sql.connect("database.db") as con3:
            cur = con3.cursor()
            cur.execute(
                "SELECT contact FROM componentTable ORDER BY fail_rate DESC")

            con3.commit()
            response = cur.fetchmany(1)
            msg = "done"
    except:
        con3.rollback()
        msg = "fail"

    finally:
        return response
        con3.close()