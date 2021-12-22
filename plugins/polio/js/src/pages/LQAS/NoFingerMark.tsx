import React, { FunctionComponent, useState, useEffect } from 'react';
import { Box } from '@material-ui/core';
import {
    Bar,
    BarChart,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    // LabelList,
    Cell,
} from 'recharts';
import { BarChartData } from './types';
import { BAR_HEIGHT } from '../../components/PercentageBarChart/constants';
import { lqasNfmTooltipFormatter } from './utils';

type Props = {
    data: BarChartData[];
    chartKey: string;
};

const NfmCustomTick: FunctionComponent<any> = ({ x, y, payload }) => {
    if (typeof payload.value === 'string') {
        const allWords = payload?.value?.split(' ') ?? [];
        const firstWord = allWords.shift();
        const valueAsWords = [firstWord, allWords.join(' ')];
        return (
            <g transform={`translate(${x},${y})`}>
                {valueAsWords.map((word, index) => (
                    <text
                        key={word + index}
                        x={0}
                        y={15 * index}
                        dy={16}
                        textAnchor="end"
                        fill="#666"
                        transform="rotate(-65)"
                    >
                        {word}
                    </text>
                ))}
            </g>
        );
    }
    return null;
};

export const NoFingerMark: FunctionComponent<Props> = ({ data, chartKey }) => {
    const [renderCount, setRenderCount] = useState(0);
    const yAxisLimit: number =
        Object.values(data)
            .map(dataEntry => dataEntry.value)
            .sort((a, b) => (a < b ? 1 : 0))[0] || 10;

    // Force render to avoid visual bug when data has length of 0
    useEffect(() => {
        setRenderCount(count => count + 1);
    }, [data]);
    return (
        <Box key={`${chartKey}${renderCount}`}>
            <ResponsiveContainer height={550} width="90%">
                <BarChart
                    data={data}
                    // layout="vertical"
                    layout="horizontal"
                    margin={{ left: 50 }}
                    barSize={BAR_HEIGHT}
                >
                    <YAxis domain={[0, yAxisLimit]} type="number" />
                    <XAxis
                        type="category"
                        dataKey="name"
                        // angle={90}
                        // tickMargin={50}
                        interval={0}
                        height={110}
                        tick={<NfmCustomTick />}
                    />
                    <Tooltip
                        payload={data}
                        formatter={lqasNfmTooltipFormatter}
                        itemStyle={{ color: 'black' }}
                    />
                    <Bar dataKey="value" minPointSize={3}>
                        {data.map((_entry, index) => {
                            return <Cell key={`cell-${index}`} fill="bisque" />;
                        })}
                        {/* <LabelList dataKey="name"  /> */}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </Box>
    );
};
