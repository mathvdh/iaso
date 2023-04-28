import React, {
    FunctionComponent,
    useState,
    useMemo,
    useCallback,
} from 'react';
import { Box, Tabs, Tab, Grid } from '@material-ui/core';
import { useDispatch } from 'react-redux';

import DownloadButtonsComponent from '../../../components/DownloadButtonsComponent';
import InputComponent from '../../../components/forms/InputComponent';
import { TableWithDeepLink } from '../../../components/tables/TableWithDeepLink';
import { ColumnSelect } from '../../instances/components/ColumnSelect';
import { ActionCell } from './ActionCell';
import { MissingInstanceDialog } from './MissingInstanceDialog';

import { redirectToReplace } from '../../../routing/actions';

import { OrgunitType } from '../../orgUnits/types/orgunitTypes';
import { OrgunitTypeRegistry } from '../types/orgunitTypes';
import { RegistryDetailParams } from '../types';
import { Column } from '../../../types/table';
import { Form } from '../../forms/types/forms';
import { OrgUnit } from '../../orgUnits/types/orgUnit';

import { useGetForms } from '../hooks/useGetForms';
import { useGetInstanceApi, useGetInstances } from '../hooks/useGetInstances';

import MESSAGES from '../messages';
import { baseUrls } from '../../../constants/urls';
import { defaultSorted, INSTANCE_METAS_FIELDS } from '../config';

type Props = {
    isLoading: boolean;
    subOrgUnitTypes: OrgunitTypeRegistry[];
    params: RegistryDetailParams;
};

export const Instances: FunctionComponent<Props> = ({
    isLoading,
    subOrgUnitTypes,
    params,
}) => {
    const [tableColumns, setTableColumns] = useState<Column[]>([]);
    const { formIds, tab } = params;
    const currentType: OrgunitTypeRegistry | undefined = useMemo(() => {
        if (subOrgUnitTypes.length > 0) {
            if (tab) {
                const existingType: OrgunitTypeRegistry | undefined =
                    subOrgUnitTypes.find(subType => `${subType.id}` === tab);
                return existingType || subOrgUnitTypes[0];
            }
            return subOrgUnitTypes[0];
        }
        return undefined;
    }, [subOrgUnitTypes, tab]);

    const dispatch = useDispatch();

    const { data: formsList, isFetching: isFetchingForms } = useGetForms();

    const { url: apiUrl } = useGetInstanceApi(params, currentType?.id);
    const { data, isFetching: isFetchingList } = useGetInstances(
        params,
        currentType?.id,
    );
    const OrgUnitsWithoutCurrentForm: OrgUnit[] = useMemo(
        () =>
            (data &&
                currentType?.orgUnits.filter(
                    orgUnit =>
                        !data.instances.find(
                            instance => instance.org_unit.id === orgUnit.id,
                        ),
                )) ||
            [],
        [currentType?.orgUnits, data],
    );
    const handleFilterChange = useCallback(
        (key: string, value: number | string) => {
            dispatch(
                redirectToReplace(baseUrls.registryDetail, {
                    ...params,
                    [key]: value,
                }),
            );
        },
        [dispatch, params],
    );

    const handleChangeTab = useCallback(
        (newType: OrgunitType) => {
            dispatch(
                redirectToReplace(baseUrls.registryDetail, {
                    ...params,
                    tab: newType.id,
                }),
            );
        },
        [dispatch, params],
    );

    const currentForm: Form | undefined = useMemo(() => {
        return formsList?.find(f => `${f.value}` === formIds)?.original;
    }, [formIds, formsList]);
    return (
        <Box>
            {currentType && !isLoading && (
                <>
                    <Tabs
                        value={currentType}
                        onChange={(_, newtab) => handleChangeTab(newtab)}
                    >
                        {subOrgUnitTypes.map(subType => (
                            <Tab
                                value={subType}
                                label={`${subType.name} (${subType.orgUnits.length})`}
                                key={subType.id}
                            />
                        ))}
                    </Tabs>
                    <Box mt={2}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={3}>
                                <InputComponent
                                    required
                                    keyValue="formIds"
                                    clearable={false}
                                    onChange={handleFilterChange}
                                    disabled={isFetchingForms}
                                    loading={isFetchingForms}
                                    value={formIds}
                                    type="select"
                                    options={formsList}
                                    label={MESSAGES.form}
                                />
                            </Grid>
                            <Grid
                                item
                                container
                                xs={12}
                                md={9}
                                justifyContent="flex-end"
                                alignItems="baseline"
                                alignContent="center"
                            >
                                {formIds && currentForm && (
                                    <ColumnSelect
                                        params={params}
                                        disabled={!formIds}
                                        periodType={currentForm.period_type}
                                        setTableColumns={newCols =>
                                            setTableColumns(newCols)
                                        }
                                        baseUrl={baseUrls.registryDetail}
                                        labelKeys={currentForm.label_keys || []}
                                        formDetails={currentForm}
                                        tableColumns={tableColumns}
                                        instanceMetasFields={
                                            INSTANCE_METAS_FIELDS
                                        }
                                        getActionCell={settings => (
                                            <ActionCell settings={settings} />
                                        )}
                                    />
                                )}
                                <Box
                                    display="flex"
                                    justifyContent="flex-end"
                                    width="100%"
                                    mt={2}
                                >
                                    <DownloadButtonsComponent
                                        csvUrl={`${apiUrl}&csv=true`}
                                        xlsxUrl={`${apiUrl}&xlsx=true`}
                                        disabled={
                                            isFetchingList || data?.count === 0
                                        }
                                    />
                                </Box>
                                <Box
                                    display="flex"
                                    justifyContent="flex-end"
                                    width="100%"
                                    mt={2}
                                >
                                    {OrgUnitsWithoutCurrentForm.length > 0 && (
                                        <MissingInstanceDialog
                                            missingOrgUnits={
                                                OrgUnitsWithoutCurrentForm
                                            }
                                            iconProps={{
                                                missingOrgUnits:
                                                    OrgUnitsWithoutCurrentForm,
                                            }}
                                        />
                                    )}
                                </Box>
                            </Grid>
                        </Grid>
                        <TableWithDeepLink
                            marginTop={false}
                            baseUrl={baseUrls.registryDetail}
                            data={data?.instances ?? []}
                            pages={data?.pages ?? 1}
                            defaultSorted={defaultSorted}
                            columns={tableColumns}
                            count={data?.count ?? 0}
                            params={params}
                            onTableParamsChange={p =>
                                dispatch(
                                    redirectToReplace(
                                        baseUrls.registryDetail,
                                        p,
                                    ),
                                )
                            }
                            extraProps={{ loading: isFetchingList }}
                        />
                    </Box>
                </>
            )}
        </Box>
    );
};
