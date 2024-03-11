import React, {
    FunctionComponent,
    useState,
    useMemo,
    useCallback,
} from 'react';
import {
    commonStyles,
    selectionInitialState,
    useSafeIntl,
    setTableSelection,
} from 'bluesquare-components';
import { Box, useTheme } from '@mui/material';
import { useDispatch } from 'react-redux';
import PaymentsIcon from '@mui/icons-material/Payments';
import TopBar from '../../components/nav/TopBarComponent';
import MESSAGES from './messages';
import { PotentialPaymentParams } from './types';
import { useGetPotentialPayments } from './hooks/requests/useGetPotentialPayments';
import { TableWithDeepLink } from '../../components/tables/TableWithDeepLink';
import { baseUrls } from '../../constants/urls';
import { PotentialPaymentsFilter } from './components/PotentialPaymentsFilter';
import { redirectTo } from '../../routing/actions';
import { usePotentialPaymentColumns } from './config/usePotentialPaymentColumns';
import { Selection } from '../orgUnits/types/selection';
import { Profile } from '../../utils/usersUtils';

type Props = {
    params: PotentialPaymentParams;
};
const baseUrl = baseUrls.potentialPayments;
export const PotentialPayments: FunctionComponent<Props> = ({ params }) => {
    const dispatch = useDispatch();

    const { data, isFetching } = useGetPotentialPayments(params);
    const { formatMessage } = useSafeIntl();
    const theme = useTheme();
    const columns = usePotentialPaymentColumns();
    const [multiActionPopupOpen, setMultiActionPopupOpen] =
        useState<boolean>(false);
    const [selection, setSelection] = useState<Selection<Profile>>(
        selectionInitialState,
    );
    const multiEditDisabled =
        !selection.selectAll && selection.selectedItems.length === 0;
    const selectionActions = useMemo(
        () => [
            {
                icon: <PaymentsIcon />,
                label: 'LABEL',
                onClick: () => setMultiActionPopupOpen(true),
                disabled: multiEditDisabled,
            },
        ],
        [multiEditDisabled, setMultiActionPopupOpen],
    );
    const handleTableSelection = useCallback(
        (selectionType, items = [], totalCount = 0) => {
            const newSelection: Selection<Profile> = setTableSelection(
                selection,
                selectionType,
                items,
                totalCount,
            );
            setSelection(newSelection);
        },
        [selection],
    );
    return (
        <>
            <TopBar
                title={formatMessage(MESSAGES.title)}
                displayBackButton={false}
            />
            <Box sx={commonStyles(theme).containerFullHeightNoTabPadded}>
                <PotentialPaymentsFilter params={params} />
                {/* @ts-ignore */}
                <TableWithDeepLink
                    marginTop={false}
                    data={data?.results ?? []}
                    pages={data?.pages ?? 1}
                    defaultSorted={[{ id: 'user__last_name', desc: false }]}
                    columns={columns}
                    count={data?.count ?? 0}
                    baseUrl={baseUrl}
                    params={params}
                    extraProps={{ loading: isFetching }}
                    // multiSelect
                    selection={selection}
                    selectionActions={selectionActions}
                    //  @ts-ignore
                    setTableSelection={(selectionType, items, totalCount) =>
                        handleTableSelection(selectionType, items, totalCount)
                    }
                    onTableParamsChange={p => dispatch(redirectTo(baseUrl, p))}
                />
            </Box>
        </>
    );
};
