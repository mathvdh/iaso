/* eslint-disable react/no-array-index-key */
/* eslint-disable camelcase */
import React, {
    FunctionComponent,
    useCallback,
    useMemo,
    useState,
} from 'react';
import { Box, Grid, useMediaQuery, useTheme } from '@mui/material';

import { groupBy } from 'lodash';
import { Paginated } from 'bluesquare-components';
import { useParamsObject } from '../../../../../../../hat/assets/js/apps/Iaso/routing/hooks/useParamsObject';
import TopBar from '../../../../../../../hat/assets/js/apps/Iaso/components/nav/TopBarComponent';
import { useStyles } from '../../../styles/theme';
import { useTableState } from '../hooks/config';
import { useBoundState } from '../../../../../../../hat/assets/js/apps/Iaso/hooks/useBoundState';
import { Optional } from '../../../../../../../hat/assets/js/apps/Iaso/types/utils';
import { useGetBudgetForCampaign } from '../hooks/api/useGetBudget';
import { useGetBudgetDetails } from '../hooks/api/useGetBudgetDetails';
import { BudgetStep } from '../types';
import { BudgetDetailsCardsLayout } from './mobile/BudgetDetailsCardsLayout';
import { BudgetDetailsTableLayout } from './BudgetDetailsTableLayout';
import { BudgetDetailsFiltersMobile } from './mobile/BudgetDetailsFiltersMobile';
import { BudgetDetailsInfos } from './BudgetDetailsInfos';
import { baseUrls } from '../../../constants/urls';
import { useGoBack } from '../../../../../../../hat/assets/js/apps/Iaso/routing/hooks/useGoBack';
import { useRedirectToReplace } from '../../../../../../../hat/assets/js/apps/Iaso/routing/routing';

type BudgetDetailsParams = {
    campaignName?: string;
    campaignId: string;
    country?: string;
    show_hidden?: string;
    action?: string;
    quickTransition?: string;
    previousStep?: string;
    transition_key?: string;
    pageSize?: string;
    page?: string;
    order?: string;
};

const baseUrl = baseUrls.budgetDetails;
export const BudgetDetails: FunctionComponent = () => {
    const params = useParamsObject(baseUrl) as BudgetDetailsParams;
    const goBack = useGoBack(baseUrls.budget);
    const redirectToReplace = useRedirectToReplace();
    const classes = useStyles();
    const { campaignName, campaignId, transition_key, ...rest } = params;
    const [showHidden, setShowHidden] = useState<boolean>(
        rest?.show_hidden === 'true',
    );

    const apiParams = useMemo(() => {
        return {
            ...rest,
            show_hidden: rest?.show_hidden === 'true',
            deletion_status: showHidden ? 'all' : undefined,
            campaign_id: campaignId,
            transition_key__in: transition_key,
        };
    }, [campaignId, rest, showHidden, transition_key]);

    const theme = useTheme();
    const isMobileLayout = useMediaQuery(theme.breakpoints.down('md'));
    const {
        data: budgetDetails,
        isFetching,
    }: { data: Paginated<BudgetStep> | undefined; isFetching: boolean } =
        useGetBudgetDetails(apiParams);

    const { data: budgetInfos } = useGetBudgetForCampaign(
        params?.campaignId as Optional<string>,
    );

    const nextSteps = useMemo(() => {
        const regular = budgetInfos?.next_transitions?.filter(
            transition =>
                transition.key !== 'override' &&
                !transition.key.includes('repeat'),
        );
        const repeat = budgetInfos?.next_transitions?.filter(
            step => step.key.includes('repeat') && step.allowed,
        );
        const toDisplay = new Set(
            regular
                ?.filter(transition => !transition.key.includes('repeat'))
                .map(transition => transition.label),
        );
        return { regular, toDisplay, repeat };
    }, [budgetInfos?.next_transitions]);

    const { resetPageToOne, columns } = useTableState({
        events: budgetDetails?.results,
        params,
        budgetDetails,
        repeatTransitions: nextSteps.repeat || [],
    });
    const [page, setPage] = useBoundState<Optional<number | string>>(
        1,
        apiParams?.page ?? 1,
    );
    const onCardPaginationChange = useCallback(
        (_value, newPage) => {
            setPage(newPage);
            redirectToReplace(baseUrls.budgetDetails, {
                ...params,
                page: newPage,
            });
        },
        [params, redirectToReplace, setPage],
    );
    const stepsList = Object.entries(
        groupBy(budgetInfos?.possible_transitions, 'label'),
    ).map(([label, items]) => {
        return { label, value: items.map(i => i.key).join(',') };
    });
    return (
        <>
            <TopBar
                title={campaignName as string}
                displayBackButton
                goBack={goBack}
            />
            {/* @ts-ignore */}
            <Box className={classes.containerFullHeightNoTabPadded}>
                <Box mb={2}>
                    <BudgetDetailsInfos
                        status={budgetInfos?.current_state?.label ?? '--'}
                        nextSteps={nextSteps}
                        categories={budgetInfos?.timeline?.categories}
                        params={params}
                        budgetDetails={budgetDetails}
                    />
                </Box>
                <Grid container spacing={isMobileLayout ? 0 : 2}>
                    {isMobileLayout && (
                        <>
                            <BudgetDetailsFiltersMobile
                                params={params}
                                showHidden={showHidden}
                                setShowHidden={setShowHidden}
                                stepsList={stepsList}
                            />
                            {budgetDetails && (
                                <BudgetDetailsCardsLayout
                                    onCardPaginationChange={
                                        onCardPaginationChange
                                    }
                                    page={page}
                                    budgetDetails={budgetDetails}
                                />
                            )}
                        </>
                    )}
                    {!isMobileLayout && (
                        <Grid item xs={12}>
                            <BudgetDetailsTableLayout
                                budgetDetails={budgetDetails}
                                params={params}
                                columns={columns}
                                isFetching={isFetching}
                                resetPageToOne={resetPageToOne}
                                showHidden={showHidden}
                                setShowHidden={setShowHidden}
                                stepsList={stepsList}
                            />
                        </Grid>
                    )}
                </Grid>
            </Box>
        </>
    );
};
