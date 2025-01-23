import { useCallback, useMemo } from 'react';
import { useQueryClient, UseQueryResult } from 'react-query';
import { getRequest } from '../../../libs/Api';
import { useSnackQuery } from '../../../libs/apiHooks';

import MESSAGES from '../../instances/messages';
import { DataSourceVersionsSynchronizationDropdown } from '../types/dataSourceVersionsSynchronization';

export const useSearchDataSourceVersionsSynchronization = () => {
    const queryClient = useQueryClient();
    const options = useMemo(
        () => ({
            enabled: false,
            select: data => {
                if (!data) return [];
                return data.results.map(item => ({
                    value: item.id,
                    label: item.name,
                }));
            },
        }),
        [],
    );
    const query = useSnackQuery({
        queryKey: ['searchDataSourceVersionsSynchronization', ''],
        queryFn: () => [],
        snackErrorMsg: MESSAGES.error,
        options,
    });

    const searchWithInput = useCallback(
        async (input: string) => {
            const newQueryKey = [
                'searchDataSourceVersionsSynchronization',
                input,
            ];
            return queryClient
                .fetchQuery(newQueryKey, async ({ queryKey }) => {
                    const [, searchTerm] = queryKey;
                    const url = `/api/datasources/sync/?fields=id,name&name__icontains=${searchTerm}`;
                    return getRequest(url);
                })
                .then(data => options.select?.(data) ?? []);
        },
        [queryClient, options],
    );

    return { ...query, searchWithInput };
};

export const useGetDataSourceVersionsSynchronizationDropdown = (
    id?: string,
): UseQueryResult<DataSourceVersionsSynchronizationDropdown[], Error> => {
    return useSnackQuery({
        queryKey: ['dataSourceVersionsSynchronizationDropdown', id],
        queryFn: () => {
            if (!id) return [];
            return getRequest(`/api/datasources/sync/${id}/?fields=id,name`);
        },
        snackErrorMsg: MESSAGES.error,
        options: {
            select: data => {
                if (data === undefined || (Array.isArray(data) && !data.length))
                    return [];
                return [
                    {
                        value: data.id,
                        label: data.name,
                    },
                ];
            },
        },
    });
};
