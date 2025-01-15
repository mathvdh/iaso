import React, { useCallback, useMemo, useState } from 'react';
import { useSafeIntl, commonStyles } from 'bluesquare-components';
import { makeStyles } from '@mui/styles';
import { Box } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import TopBar from '../../components/nav/TopBarComponent';
import MESSAGES from './messages';
import { useGetPages } from './hooks/useGetPages';
import { useRemovePage } from './hooks/useRemovePage';
import DeleteConfirmDialog from './components/DeleteConfirmDialog';
import CreateEditDialog from './components/CreateEditDialog';
import PageActions from './components/PageActions';
import PageAction from './components/PageAction';
import { TableWithDeepLink } from '../../components/tables/TableWithDeepLink.tsx';
import { useParamsObject } from '../../routing/hooks/useParamsObject.tsx';
import { baseUrls } from '../../constants/urls.ts';
import Filters from './components/Filters';
import { usePagesColumns } from './config';

const DEFAULT_PAGE_SIZE = 10;
const DEFAULT_PAGE = 1;
const DEFAULT_ORDER = '-updated_at';

const useStyles = makeStyles(theme => ({
    ...commonStyles(theme),
}));

const Pages = () => {
    const { formatMessage } = useSafeIntl();
    const classes = useStyles();
    const params = useParamsObject(baseUrls.pages);
    const [selectedPageSlug, setSelectedPageSlug] = useState();
    const [isCreateEditDialogOpen, setIsCreateEditDialogOpen] = useState(false);
    const [isConfirmDeleteDialogOpen, setIsConfirmDeleteDialogOpen] =
        useState(false);

    const tableParams = useMemo(() => {
        return {
            order: params.order ?? DEFAULT_ORDER,
            pageSize: params.pageSize ?? DEFAULT_PAGE_SIZE,
            page: params.page ?? DEFAULT_PAGE,
            search: params.search,
        };
    }, [params]);

    const openCreateEditDialog = useCallback(() => {
        setIsCreateEditDialogOpen(true);
    }, [setIsCreateEditDialogOpen]);

    const handleClickCreateButton = () => {
        setSelectedPageSlug(undefined);
        openCreateEditDialog();
    };

    const closeCreateEditDialog = () => {
        setSelectedPageSlug(undefined);
        setIsCreateEditDialogOpen(false);
    };

    const closeDeleteConfirmDialog = () => {
        setIsConfirmDeleteDialogOpen(false);
    };

    const { mutate: removePage } = useRemovePage();

    const { data: pages, isFetching } = useGetPages(tableParams);

    const selectedPage = pages?.results?.find(
        result => result.slug === selectedPageSlug,
    );

    const handleDeleteConfirmDialogConfirm = () => {
        removePage(selectedPage?.slug, {
            onSuccess: () => {
                closeDeleteConfirmDialog();
            },
        });
    };

    const columns = usePagesColumns(
        setSelectedPageSlug,
        setIsCreateEditDialogOpen,
        setIsConfirmDeleteDialogOpen,
    );

    return (
        <>
            <CreateEditDialog
                selectedPage={selectedPage}
                isOpen={isCreateEditDialogOpen}
                onClose={closeCreateEditDialog}
            />
            <DeleteConfirmDialog
                isOpen={isConfirmDeleteDialogOpen}
                onClose={closeDeleteConfirmDialog}
                onConfirm={handleDeleteConfirmDialogConfirm}
            />
            <TopBar title={formatMessage(MESSAGES.pages)} />
            <Box className={classes.containerFullHeightNoTabPadded}>
                <Filters params={params} />
                <Box mt={4}>
                    <PageActions>
                        <PageAction
                            icon={AddIcon}
                            onClick={handleClickCreateButton}
                        >
                            {formatMessage(MESSAGES.create)}
                        </PageAction>
                    </PageActions>
                </Box>

                <TableWithDeepLink
                    data={pages?.results ?? []}
                    pages={pages?.pages}
                    count={pages?.count}
                    params={tableParams}
                    columns={columns}
                    baseUrl="/pages"
                    extraProps={{
                        loading: isFetching,
                    }}
                />
            </Box>
        </>
    );
};

export default Pages;
