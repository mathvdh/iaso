import React, { FunctionComponent, useCallback, useMemo } from 'react';
import { Box, Grid } from '@mui/material';
import { useSafeIntl } from 'bluesquare-components';
import { FilterButton } from '../../../../components/FilterButton';
import { useFilterState } from '../../../../hooks/useFilterState';
import InputComponent from '../../../../components/forms/InputComponent';
import { baseUrls } from '../../../../constants/urls';
import MESSAGES from '../messages';
import { OrgUnitTreeviewModal } from '../../components/TreeView/OrgUnitTreeviewModal';
import { useGetOrgUnit } from '../../components/TreeView/requests';
// IA-3641 uncomment when UI has been refactored to limlit size of API call
// import { useGetGroupDropdown } from '../../hooks/requests/useGetGroups';
import { useGetOrgUnitTypesDropdownOptions } from '../../orgUnitTypes/hooks/useGetOrgUnitTypesDropdownOptions';
import { DropdownOptions } from '../../../../types/utils';
import DatesRange from '../../../../components/filters/DatesRange';
import { useGetForms } from '../../../workflows/hooks/requests/useGetForms';
import { ApproveOrgUnitParams } from '../types';
import { AsyncSelect } from '../../../../components/forms/AsyncSelect';
import { getUsersDropDown } from '../../../instances/hooks/requests/getUsersDropDown';
import { useGetProfilesDropdown } from '../../../instances/hooks/useGetProfilesDropdown';
import { useGetUserRolesDropDown } from '../../../userRoles/hooks/requests/useGetUserRoles';
import { useGetProjectsDropdownOptions } from '../../../projects/hooks/requests';
import { usePaymentStatusOptions } from '../hooks/api/useGetPaymentStatusOptions';

const baseUrl = baseUrls.orgUnitsChangeRequest;
type Props = { params: ApproveOrgUnitParams };

export const ReviewOrgUnitChangesFilter: FunctionComponent<Props> = ({
    params,
}) => {
    const { formatMessage } = useSafeIntl();
    const { filters, handleSearch, handleChange, filtersUpdated } =
        useFilterState({ baseUrl, params });
    const { data: initialOrgUnit } = useGetOrgUnit(params.parent_id);
    // IA-3641 hard coding values fro groups dropdown until refactor
    // const { data: groupOptions, isLoading: isLoadingGroups } =
    //     useGetGroupDropdown({});
    const groupOptions = [];
    const isLoadingGroups = false;
    // IA-3641 -----END
    const { data: orgUnitTypeOptions, isLoading: isLoadingTypes } =
        useGetOrgUnitTypesDropdownOptions();
    const { data: forms, isFetching: isLoadingForms } = useGetForms();
    const { data: selectedUsers } = useGetProfilesDropdown(filters.userIds);
    const { data: userRoles, isFetching: isFetchingUserRoles } =
        useGetUserRolesDropDown();

    const { data: allProjects, isFetching: isFetchingProjects } =
        useGetProjectsDropdownOptions();
    const { data: paymentStatuses, isFetching: isFetchingPaymentStatuses } =
        usePaymentStatusOptions();
    const formOptions = useMemo(
        () =>
            forms?.map(form => ({
                label: form.name,
                value: form.id,
            })) || [],
        [forms],
    );
    const statusOptions: DropdownOptions<string>[] = useMemo(
        () => [
            {
                label: formatMessage(MESSAGES.new),
                value: 'new',
            },
            {
                label: formatMessage(MESSAGES.rejected),
                value: 'rejected',
            },
            {
                label: formatMessage(MESSAGES.approved),
                value: 'approved',
            },
        ],
        [formatMessage],
    );
    const handleChangeUsers = useCallback(
        (keyValue, newValue) => {
            const joined = newValue?.map(r => r.value)?.join(',');
            handleChange(keyValue, joined);
        },
        [handleChange],
    );

    return (
        <Grid container spacing={2}>
            <Grid item xs={12} md={4} lg={3}>
                <InputComponent
                    keyValue="projectIds"
                    onChange={handleChange}
                    value={filters.projectIds}
                    type="select"
                    options={allProjects}
                    label={MESSAGES.projects}
                    loading={isFetchingProjects}
                    onEnterPressed={handleSearch}
                    clearable
                    multi
                />
                <InputComponent
                    type="select"
                    multi
                    clearable
                    keyValue="status"
                    value={filters.status}
                    onChange={handleChange}
                    options={statusOptions}
                    labelString={formatMessage(MESSAGES.status)}
                />
                <InputComponent
                    type="select"
                    multi
                    clearable
                    keyValue="groups"
                    value={filters.groups}
                    onChange={handleChange}
                    options={groupOptions}
                    loading={isLoadingGroups}
                    labelString={formatMessage(MESSAGES.group)}
                    disabled
                    helperText={formatMessage(MESSAGES.featureDisabled)}
                />
            </Grid>
            <Grid item xs={12} md={4} lg={3}>
                <Box id="ou-tree-input">
                    <OrgUnitTreeviewModal
                        toggleOnLabelClick={false}
                        titleMessage={MESSAGES.parent}
                        onConfirm={orgUnit => {
                            handleChange('parent_id', orgUnit?.id);
                        }}
                        initialSelection={initialOrgUnit}
                    />
                </Box>
                <InputComponent
                    type="select"
                    multi
                    clearable
                    keyValue="org_unit_type_id"
                    value={filters.org_unit_type_id}
                    onChange={handleChange}
                    loading={isLoadingTypes}
                    options={orgUnitTypeOptions}
                    labelString={formatMessage(MESSAGES.orgUnitType)}
                />
                <InputComponent
                    type="select"
                    multi
                    clearable
                    keyValue="forms"
                    value={filters.forms}
                    onChange={handleChange}
                    options={formOptions}
                    loading={isLoadingForms}
                    labelString={formatMessage(MESSAGES.forms)}
                />
            </Grid>
            <Grid item xs={12} md={4} lg={3}>
                <Box mt={2}>
                    <AsyncSelect
                        keyValue="userIds"
                        label={MESSAGES.user}
                        value={selectedUsers ?? ''}
                        onChange={handleChangeUsers}
                        debounceTime={500}
                        multi
                        fetchOptions={input => getUsersDropDown(input)}
                    />
                </Box>
                <InputComponent
                    type="select"
                    multi
                    clearable
                    keyValue="userRoles"
                    value={filters.userRoles}
                    onChange={handleChange}
                    loading={isFetchingUserRoles}
                    options={userRoles}
                    labelString={formatMessage(MESSAGES.userRoles)}
                />
                <InputComponent
                    keyValue="withLocation"
                    clearable
                    onChange={handleChange}
                    value={filters.withLocation || null}
                    type="select"
                    options={[
                        {
                            label: formatMessage(MESSAGES.with),
                            value: 'true',
                        },
                        {
                            label: formatMessage(MESSAGES.without),
                            value: 'false',
                        },
                    ]}
                />
                <InputComponent
                    label={MESSAGES.location}
                    type="select"
                    clearable
                    keyValue="paymentStatus"
                    value={filters.paymentStatus}
                    onChange={handleChange}
                    loading={isFetchingPaymentStatuses}
                    options={paymentStatuses}
                    labelString={formatMessage(MESSAGES.paymentStatus)}
                />
            </Grid>

            <Grid item xs={12} md={4} lg={3}>
                <DatesRange
                    xs={12}
                    sm={12}
                    md={12}
                    lg={12}
                    keyDateFrom="created_at_after"
                    keyDateTo="created_at_before"
                    onChangeDate={handleChange}
                    dateFrom={filters.created_at_after}
                    dateTo={filters.created_at_before}
                    labelFrom={MESSAGES.createdDateFrom}
                    labelTo={MESSAGES.createdDateTo}
                />
                <Box mt={2} display="flex" justifyContent="flex-end">
                    <FilterButton
                        disabled={!filtersUpdated}
                        onFilter={handleSearch}
                    />
                </Box>
            </Grid>
        </Grid>
    );
};
