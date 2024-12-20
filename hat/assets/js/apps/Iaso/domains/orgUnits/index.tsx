import React, {
    FunctionComponent,
    useMemo,
    useState,
    useEffect,
    useCallback,
} from 'react';
import { Box, Tabs, Tab } from '@mui/material';
import { makeStyles } from '@mui/styles';
import {
    commonStyles,
    useSafeIntl,
    LoadingSpinner,
    useSkipEffectOnMount,
    makeRedirectionUrl,
} from 'bluesquare-components';
import { useQueryClient } from 'react-query';

// COMPONENTS
import { useNavigate } from 'react-router-dom';
import DownloadButtonsComponent from '../../components/DownloadButtonsComponent';
import { OrgUnitFiltersContainer } from './components/OrgUnitFiltersContainer';
import TopBar from '../../components/nav/TopBarComponent';
import { OrgUnitsMap } from './components/OrgUnitsMap';
import { TableList } from './components/TableList';
// COMPONENTS

// TYPES
import { OrgUnitParams } from './types/orgUnit';
import { Search } from './types/search';
// TYPES

// UTILS
import { decodeSearch } from './utils';
import { convertObjectToString } from '../../utils/dataManipulation';
import { getChipColors } from '../../constants/chipColors';
// UTILS

// CONSTANTS
import { baseUrls } from '../../constants/urls';
import MESSAGES from './messages';
import { MENU_HEIGHT_WITHOUT_TABS } from '../../constants/uiConstants';
// CONSTANTS

// HOOKS
import {
    useGetOrgUnits,
    useGetOrgUnitsLocations,
} from './hooks/requests/useGetOrgUnits';
import { useBulkSaveOrgUnits } from './hooks/requests/useBulkSaveOrgUnits';
import { useGetApiParams } from './hooks/useGetApiParams';
import { useParamsObject } from '../../routing/hooks/useParamsObject';
// HOOKS

const useStyles = makeStyles(theme => ({
    ...commonStyles(theme),
    container: {
        width: '100%',
        height: `calc(100vh - ${MENU_HEIGHT_WITHOUT_TABS}px)`,
        padding: 0,
        margin: 0,
        overflow: 'auto',
        backgroundColor: 'white',
        position: 'relative',
        top: 48,
        '& .MuiSpeedDial-directionUp, &.MuiSpeedDial-directionLeft': {
            position: 'fixed',
        },
    },
    tabs: {
        ...commonStyles(theme).tabs,
        padding: 0,
    },
    hiddenOpacity: {
        position: 'absolute',
        top: '0px',
        left: '0px',
        zIndex: '-100',
        opacity: '0',
        width: '100%',
    },
}));

// type Props = {
//     params: OrgUnitParams;
// };

const baseUrl = baseUrls.orgUnits;
export const OrgUnits: FunctionComponent = () => {
    // HOOKS
    const params = useParamsObject(baseUrl) as unknown as OrgUnitParams;
    const queryClient = useQueryClient();
    const navigate = useNavigate();
    const classes: Record<string, string> = useStyles();
    const { formatMessage } = useSafeIntl();
    // HOOKS

    // STATE
    const [resetPageToOne, setResetPageToOne] = useState<string>('');
    const [deletedTab, setDeletedTab] = useState<boolean>(false);
    const [refresh, setRefresh] = useState<boolean>(false);
    const [tab, setTab] = useState<string>(params.tab ?? 'list');
    // STATE

    // MEMO
    const searches: [Search] = useMemo(() => {
        return decodeSearch(decodeURI(params.searches));
    }, [params.searches]);
    const isSearchActive: boolean = useMemo(
        () => params.searchActive === 'true',
        [params.searchActive],
    );
    // MEMO

    // CUSTOM HOOKS
    const { getUrl, apiParams } = useGetApiParams(searches, params);
    const { apiParams: apiParamsLocations } = useGetApiParams(
        searches,
        params,
        true,
    );
    // CUSTOM HOOKS

    // REQUESTS HOOKS
    const { mutateAsync: saveMulti, isLoading: isSavingMulti } =
        useBulkSaveOrgUnits();
    const {
        data: orgUnitsData,
        isFetching: isFetchingOrgUnits,
        refetch: fetchOrgUnits,
    } = useGetOrgUnits({
        params: apiParams,
        isSearchActive,
    });
    const {
        data: orgUnitsDataLocation,
        isFetching: isFetchingOrgUnitsDataLocation,
        refetch: fetchOrgUnitsLocations,
    } = useGetOrgUnitsLocations({
        params: apiParamsLocations,
        searches,
        isSearchActive,
    });
    // REQUESTS HOOKS

    const getSearchColor = useCallback(
        currentSearchIndex => {
            const currentSearch = searches[currentSearchIndex];
            let currentColor;
            if (currentSearch) {
                currentColor = currentSearch.color;
            }
            if (!currentColor) {
                currentColor = getChipColors(currentSearchIndex);
            } else {
                currentColor = `#${currentColor}`;
            }
            return currentColor;
        },
        [searches],
    );

    const handleSearch = useCallback(() => {
        if (isSearchActive) {
            fetchOrgUnits();
            fetchOrgUnitsLocations();
        }
    }, [fetchOrgUnits, fetchOrgUnitsLocations, isSearchActive]);

    const onSearch = useCallback(
        newParams => {
            // handleTableSelection('reset');
            const tempParams = {
                ...newParams,
                searches: JSON.stringify(newParams.searches),
            };
            if (newParams.searchActive !== 'true') {
                tempParams.searchActive = true;
            }
            setResetPageToOne(convertObjectToString(tempParams));
            navigate(makeRedirectionUrl(baseUrl, tempParams), {
                replace: true,
            });
            setRefresh(true);
        },
        [navigate],
    );
    // TABS
    const handleChangeTab = useCallback(
        newtab => {
            setTab(newtab);
            const newParams = {
                ...params,
                tab: newtab,
            };
            navigate(makeRedirectionUrl(baseUrl, newParams));
        },
        [params, navigate],
    );
    // TABS

    // onload, if searchActive is true and cache empty => set launch search
    useEffect(() => {
        if (isSearchActive) {
            const cachedOrgUnits = queryClient.getQueryData(['orgunits']);
            const cachedLocations = queryClient.getQueryData([
                'orgunitslocations',
            ]);
            if (!cachedOrgUnits || !cachedLocations) {
                handleSearch();
            }
        }
    }, [handleSearch, isSearchActive, queryClient]);

    // trigger search on order, page size and page
    useSkipEffectOnMount(() => {
        handleSearch();
    }, [params.order, params.page, params.pageSize]);

    // trigger search after delete tab redirection
    useSkipEffectOnMount(() => {
        if (isSearchActive && deletedTab) {
            setDeletedTab(false);
            handleSearch();
        }
    }, [apiParams.searches]);

    useSkipEffectOnMount(() => {
        if (refresh) {
            setRefresh(false);
            handleSearch();
        }
    }, [searches, refresh]);

    const isLoading =
        isFetchingOrgUnits ||
        isSavingMulti ||
        (tab === 'map' && isFetchingOrgUnitsDataLocation);
    return (
        <>
            {isLoading && <LoadingSpinner fixed={false} absolute />}
            <TopBar title={formatMessage(MESSAGES.title)} />

            <Box className={classes.container}>
                <OrgUnitFiltersContainer
                    params={params}
                    onSearch={onSearch}
                    currentTab={tab}
                    paramsSearches={searches || []}
                    counts={(!isLoading && orgUnitsData?.counts) || []}
                    setDeletedTab={setDeletedTab}
                />
                {tab === 'list' &&
                    orgUnitsData &&
                    orgUnitsData?.orgunits?.length > 0 && (
                        <Box
                            mb={2}
                            mt={2}
                            mr={4}
                            display="flex"
                            justifyContent="flex-end"
                        >
                            <DownloadButtonsComponent
                                csvUrl={getUrl(true, 'csv')}
                                xlsxUrl={getUrl(true, 'xlsx')}
                                gpkgUrl={getUrl(true, 'gpkg')}
                            />
                        </Box>
                    )}
                <Box px={4}>
                    {orgUnitsData && (
                        <>
                            <Tabs
                                value={tab}
                                classes={{
                                    root: classes.tabs,
                                }}
                                className={classes.marginBottom}
                                indicatorColor="primary"
                                onChange={(event, newtab) =>
                                    handleChangeTab(newtab)
                                }
                            >
                                <Tab
                                    value="list"
                                    label={formatMessage(MESSAGES.list)}
                                />
                                <Tab
                                    value="map"
                                    label={formatMessage(MESSAGES.map)}
                                />
                            </Tabs>
                            {tab === 'list' && (
                                <TableList
                                    params={params}
                                    saveMulti={saveMulti}
                                    resetPageToOne={resetPageToOne}
                                    orgUnitsData={orgUnitsData}
                                />
                            )}

                            <div
                                className={
                                    tab === 'map' ? '' : classes.hiddenOpacity
                                }
                            >
                                <div className={classes.containerMarginNeg}>
                                    <OrgUnitsMap
                                        getSearchColor={getSearchColor}
                                        orgUnits={
                                            orgUnitsDataLocation || {
                                                locations: [],
                                                shapes: [],
                                            }
                                        }
                                    />
                                </div>
                            </div>
                        </>
                    )}
                </Box>
            </Box>
        </>
    );
};
