import React, { FunctionComponent, useMemo } from 'react';
import { useSafeIntl } from 'bluesquare-components';
import MESSAGES from '../../../../constants/messages';
import { makeLqasMapLegendItems } from '../utils';
import { LqasImCountryMap } from '../../shared/Map/LqasImCountryMap';
import { lqasDistrictColors } from '../constants';
import { Side } from '../../../../constants/types';

const getMainLayerStyles = shape => {
    return lqasDistrictColors[shape.status];
};

type Props = {
    round: number;
    campaigns?: any[];
    selectedCampaign?: string;
    countryId?: number;
    data?: any;
    isFetchingGeoJson?: boolean;
    mainLayer: any;
    isFetching?: boolean;
    disclaimerData?: Record<string, unknown> | null | undefined;
    regionShapes: any;
    isFetchingRegions: boolean;
    side: Side;
};

export const LqasCountryMap: FunctionComponent<Props> = ({
    round,
    side,
    selectedCampaign,
    countryId = undefined,
    campaigns = [],
    data,
    isFetching = false,
    disclaimerData = {},
    isFetchingGeoJson = false,
    mainLayer,
    regionShapes,
    isFetchingRegions = false,
}) => {
    const { formatMessage } = useSafeIntl();

    const legendItems = useMemo(() => {
        return makeLqasMapLegendItems(formatMessage)(
            data,
            selectedCampaign,
            round,
        );
    }, [data, selectedCampaign, round, formatMessage]);

    const title = formatMessage(MESSAGES.lqasResults);

    return (
        <LqasImCountryMap
            key={`${countryId}-${side}`}
            name={`LQASIMMap${round}-LQAS-${countryId}-${side}`}
            regionShapes={regionShapes}
            mainLayer={mainLayer}
            round={round}
            isFetchingRegions={isFetchingRegions}
            title={title}
            selectedCampaign={selectedCampaign}
            legendItems={legendItems}
            campaigns={campaigns}
            data={data}
            isFetching={isFetching}
            isFetchingGeoJson={isFetchingGeoJson}
            disclaimerData={disclaimerData}
            getMainLayerStyles={getMainLayerStyles}
        />
    );
};
