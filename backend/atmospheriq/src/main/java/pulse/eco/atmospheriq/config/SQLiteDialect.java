/*
package pulse.eco.atmospheriq.config;

import org.hibernate.dialect.Dialect;

import java.sql.Types;

public class SQLiteDialect extends Dialect {

    public SQLiteDialect() {
        super();
    }

    @Override
    public String getJdbcTypeName(int code) {
        switch (code) {
            case Types.INTEGER:
                return "INTEGER";
            case Types.VARCHAR:
                return "VARCHAR";
            case Types.BLOB:
                return "BLOB";
            case Types.CLOB:
                return "TEXT";
            default:
                return super.getJdbcTypeName(code);
        }
    }

    @Override
    public boolean supportsIdentityColumns() {
        return true;
    }

    @Override
    public boolean hasAlterTable() {
        return false; // SQLite doesn't support full ALTER TABLE operations.
    }
}*/
