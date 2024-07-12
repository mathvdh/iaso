/* eslint-disable camelcase */
import { UseQueryResult } from 'react-query';
import { Pagination } from 'bluesquare-components';
import { getRequest } from '../../../../libs/Api';
import { useSnackQuery } from '../../../../libs/apiHooks';
import { makeUrlWithParams } from '../../../../libs/utils';
import {
    UserRoleParams,
    UserRolesFilterParams,
    UserRole,
} from '../../types/userRoles';
import { DropdownOptions } from '../../../../types/utils';
import MESSAGES from '../../messages';

type UserRolesList = Pagination & {
    results: UserRole[];
};

const getUserRoles = async (
    options: UserRoleParams | UserRolesFilterParams,
): Promise<UserRolesList> => {
    const { pageSize, order, page, ...params } = options as Record<string, any>;

    params.limit = pageSize || 20;
    params.order = order || 'group__name';
    params.page = page || 1;
    if (params.select) {
        delete params.select;
    }
    const url = makeUrlWithParams('/api/userroles', params);
    return getRequest(url) as Promise<UserRolesList>;
};

export const useGetUserRoles = (
    options: UserRoleParams | UserRolesFilterParams,
): UseQueryResult<UserRolesList, Error> => {
    const { select } = options as Record<string, any>;
    return useSnackQuery({
        queryKey: ['userRolesList', options],
        queryFn: () => getUserRoles(options),
        snackErrorMsg: undefined,
        options: {
            select,
        },
    });
};

export const useGetUserRolesDropDown = (): UseQueryResult<
    DropdownOptions<number>[],
    Error
> => {
    return useSnackQuery({
        queryKey: ['user_roles_dropdown'],
        queryFn: () => getRequest('/api/userroles/'),
        snackErrorMsg: MESSAGES.userRolesDropDownError,
        options: {
            staleTime: 1000 * 60 * 15, // in MS
            cacheTime: 1000 * 60 * 5,
            select: data => {
                return (
                    data?.results?.map((userRole: UserRole) => {
                        return {
                            value: userRole.id,
                            label: userRole.name,
                            original: userRole,
                        };
                    }) ?? []
                );
            },
        },
    });
};
