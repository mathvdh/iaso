import React, { memo } from 'react';
import { TableBody, TableRow, TableCell } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { formatLabel } from '../../utils';
import { FileContent } from '../../types/instance';

type TableBodyProps = {
    fileContent: FileContent;
    fileDescriptor?: Record<string, any>;
};
const useStyles = makeStyles(theme => ({
    tableCell: {
        backgroundColor: 'transparent',
        borderTop: 'none !important',
        borderLeft: 'none !important',
        borderRight: 'none !important',
        // @ts-ignore
        borderBottom: `1px solid ${theme.palette.ligthGray.border}  !important`,
    },
    tableCellLabelName: {
        // @ts-ignore
        color: theme.palette.mediumGray.main,
    },
    highlightedRow: {
        backgroundColor: '#f7eb9c',
    },
}));

const InstanceLogContentBodyTable = memo(
    ({ fileContent, fileDescriptor }: TableBodyProps) => {
        const classes = useStyles();

        return (
            <TableBody>
                {fileContent.logA &&
                    fileContent.logB &&
                    fileContent?.fields.map(question => {
                        const isRelevantQuestion = ![
                            'meta',
                            'instanceID',
                        ].includes(question.name);
                        const hasLogContent =
                            fileContent.logA.json[question.name] ||
                            fileContent.logB.json[question.name];
                        const field = fileDescriptor?.children.find(
                            child => child.name === question.name,
                        );
                        const isValuesDifferent =
                            fileContent.logA.json[question.name] !==
                            fileContent.logB.json[question.name];

                        if (isRelevantQuestion && hasLogContent) {
                            return (
                                <TableRow
                                    key={question.name}
                                    className={
                                        isValuesDifferent
                                            ? classes.highlightedRow
                                            : undefined
                                    }
                                >
                                    <TableCell
                                        className={classes.tableCell}
                                        align="left"
                                    >
                                        <div>
                                            {fileDescriptor?.children && field
                                                ? formatLabel(field)
                                                : question.name}
                                        </div>
                                        <span
                                            className={
                                                classes.tableCellLabelName
                                            }
                                        >
                                            {question.name}
                                        </span>
                                    </TableCell>
                                    <TableCell
                                        className={classes.tableCell}
                                        align="left"
                                    >
                                        {fileContent?.logA.json[question.name]}
                                    </TableCell>
                                    <TableCell
                                        className={classes.tableCell}
                                        align="left"
                                    >
                                        {fileContent?.logB.json[question.name]}
                                    </TableCell>
                                </TableRow>
                            );
                        }
                        return null;
                    })}
            </TableBody>
        );
    },
);

export default InstanceLogContentBodyTable;