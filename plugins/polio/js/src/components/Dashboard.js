import { Box, makeStyles } from '@material-ui/core';
import { useMemo } from 'react';
import { useTable } from 'react-table';

import commonStyles from '../styles/common';
import { TableHeader } from './Table/TableHeader';
import { TableCell } from './Table/TableCell';

const useStyles = makeStyles(theme => ({
    ...commonStyles(theme),
    table: {
        borderSpacing: 0,
        border: '1px solid rgba(0,0,0,0.1)',
    },
    tableHeader: {
        display: 'flex',
        boxShadow: '0 2px 15px 0 rgb(0 0 0 / 15%)',
    },
    tableRow: {
        display: 'flex',
    },
}));

export const Dashboard = () => {
    const classes = useStyles();

    const data = useMemo(
        () => [
            {
                name: 'DRC-39DS-01-2021',
                notificationDate: '02-20-2021',
                status: 'Risk Assessment Required',
                duration: '4',
                actions: 'Edit',
            },
        ],
        [],
    );

    const columns = useMemo(
        () => [
            {
                Header: 'Name',
                accessor: 'name',
            },
            {
                Header: 'cVDPV2 Notification Date',
                accessor: 'notificationDate',
            },
            {
                Header: 'Status',
                accessor: 'status',
            },
            {
                Header: 'Duration (days)',
                accessor: 'duration',
            },
            {
                Header: 'Actions',
                accessor: 'actions',
            },
        ],
        [],
    );

    const tableInstance = useTable({ columns, data });

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = tableInstance;

    return (
        <Box className={classes.containerFullHeightNoTabPadded}>
            <table className={classes.table} {...getTableProps()}>
                <thead>
                    {headerGroups.map(headerGroup => (
                        <tr
                            className={classes.tableHeader}
                            {...headerGroup.getHeaderGroupProps()}
                        >
                            {headerGroup.headers.map(column => (
                                <TableHeader {...column.getHeaderProps()}>
                                    {column.render('Header')}
                                </TableHeader>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map(row => {
                        prepareRow(row);
                        return (
                            <tr
                                className={classes.tableRow}
                                {...row.getRowProps()}
                            >
                                {row.cells.map(cell => {
                                    return (
                                        <TableCell {...cell.getCellProps()}>
                                            {cell.render('Cell')}
                                        </TableCell>
                                    );
                                })}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </Box>
    );
};
