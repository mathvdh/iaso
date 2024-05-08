import React, { FunctionComponent, useState, useCallback } from 'react';
import {
    useSafeIntl,
    useSkipEffectOnMount,
    LoadingSpinner,
} from 'bluesquare-components';
import { Box, useMediaQuery, useTheme, Collapse, Grid } from '@mui/material';
import { makeStyles } from '@mui/styles';
import SearchIcon from '@mui/icons-material/Search';
import { Pagination } from '@mui/lab';

// @ts-ignore
import TopBar from 'Iaso/components/nav/TopBarComponent';
import { TableWithDeepLink } from '../../../../../../hat/assets/js/apps/Iaso/components/tables/TableWithDeepLink';

import { BudgetFilters } from './BudgetFilters';
import { BudgetCard } from './cards/BudgetCard';
import { useBudgetColumns } from './hooks/config';
import { CsvButton } from '../../../../../../hat/assets/js/apps/Iaso/components/Buttons/CsvButton';
import {
    useBudgetParams,
    useGetBudgets,
    useGetWorkflowStatesForDropdown,
} from './hooks/api/useGetBudget';
import { Budget } from './types';
import { useStyles } from '../../styles/theme';
import MESSAGES from '../../constants/messages';
import { baseUrls } from '../../constants/urls';
import { useParamsObject } from '../../../../../../hat/assets/js/apps/Iaso/routing/hooks/useParamsObject';
import { useRedirectToReplace } from '../../../../../../hat/assets/js/apps/Iaso/routing/routing';

const getCsvParams = (apiParams: Record<string, any>): string => {
    const {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        pageSize,
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        page,
        ...paramsForCsv
    } = apiParams;
    const filteredParams: Record<string, any> = Object.fromEntries(
        Object.entries(paramsForCsv).filter(
            // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
            ([_key, value]) => value !== undefined,
        ),
    );
    return new URLSearchParams(filteredParams).toString();
};

const usePaginationStyles = makeStyles({
    pagination: {
        '&.MuiPagination-root > .MuiPagination-ul': {
            justifyContent: 'center',
        },
    },
    alignRight: { textAlign: 'right' },
});

type Params = {
    search?: string;
    budget_current_state_key__in?: string;
    roundStartFrom?: string;
    roundStartTo?: string;
    country__id__in?: string;
    orgUnitGroups?: string;
    order?: string;
    pageSize?: string;
    page?: string;
};
const baseUrl = baseUrls.budget;

export const BudgetList: FunctionComponent = () => {
    const params = useParamsObject(baseUrl) as Params;
    const { formatMessage } = useSafeIntl();
    const paginationStyle = usePaginationStyles();
    const classes = useStyles();
    const [expand, setExpand] = useState<boolean>(false);
    const redirectToReplace = useRedirectToReplace();

    const apiParams = useBudgetParams(params); // TODO fix and export type
    const csvParams = getCsvParams(apiParams);

    const { data: budgets, isFetching } = useGetBudgets(apiParams);
    const columns = useBudgetColumns();
    const theme = useTheme();
    const isMobileLayout = useMediaQuery(theme.breakpoints.down('md'));

    useSkipEffectOnMount(() => {
        const newParams = {
            ...apiParams,
        };
        delete newParams.page;
        delete newParams.order;
    }, [apiParams.pageSize, apiParams.search]);

    const onCardPaginationChange = useCallback(
        (_value, newPage) => {
            redirectToReplace(baseUrl, { ...apiParams, page: newPage });
        },
        [apiParams, redirectToReplace],
    );
    const { data: possibleStates } = useGetWorkflowStatesForDropdown();

    return (
        <>
            <TopBar
                title={formatMessage(MESSAGES.budget)}
                displayBackButton={false}
            >
                {isMobileLayout && (
                    <Box
                        position="absolute"
                        top={theme.spacing(2)}
                        right={theme.spacing(2)}
                    >
                        <SearchIcon
                            onClick={() => {
                                setExpand(value => !value);
                            }}
                        />
                    </Box>
                )}
            </TopBar>
            {/* @ts-ignore */}
            <Box className={classes.containerFullHeightNoTabPadded}>
                {isMobileLayout && (
                    <Collapse in={expand}>
                        <BudgetFilters
                            params={params}
                            buttonSize="small"
                            statesList={possibleStates}
                        />
                        <Grid container justifyContent="flex-end">
                            <Box mb={4}>
                                <CsvButton
                                    csvUrl={`/api/polio/budget/export_csv/?${csvParams}`}
                                />
                            </Box>
                        </Grid>
                    </Collapse>
                )}

                {!isMobileLayout && (
                    <>
                        <BudgetFilters
                            params={params}
                            statesList={possibleStates}
                        />
                        <Box mb={2} className={paginationStyle.alignRight}>
                            <CsvButton
                                csvUrl={`/api/polio/budget/export_csv/?${csvParams}`}
                            />
                        </Box>

                        <TableWithDeepLink
                            data={budgets?.results ?? []}
                            count={budgets?.count}
                            pages={budgets?.pages}
                            params={apiParams}
                            columns={columns}
                            baseUrl={baseUrl}
                            marginTop={false}
                            extraProps={{
                                loading: isFetching,
                                apiParams,
                            }}
                        />
                    </>
                )}
                {isMobileLayout && (
                    <>
                        {isFetching && <LoadingSpinner />}
                        {budgets?.results &&
                            budgets.results.map((budget: Budget) => (
                                <Box key={budget.id} mb={1}>
                                    <BudgetCard budget={budget} />
                                </Box>
                            ))}

                        {budgets && (
                            <Pagination
                                className={paginationStyle.pagination}
                                page={budgets.page}
                                count={budgets.pages}
                                showLastButton
                                showFirstButton
                                onChange={onCardPaginationChange}
                                hidePrevButton={false}
                                hideNextButton={false}
                                size="small"
                            />
                        )}
                    </>
                )}
            </Box>
        </>
    );
};
