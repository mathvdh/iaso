import { UseMutationResult } from 'react-query';
import { postRequest } from '../../../../libs/Api';
import { useSnackMutation } from '../../../../libs/apiHooks';

import { FollowUps } from '../../types/workflows';

const bulkUpdateWorkflowFollowUp = async (data: FollowUps[]): Promise<any> =>
    postRequest('/api/workflowfollowups/bulkupdate/', data);

export const useBulkUpdateWorkflowFollowUp = (
    onSuccess?: () => void,
): UseMutationResult =>
    useSnackMutation({
        mutationFn: (data: FollowUps[]) => bulkUpdateWorkflowFollowUp(data),
        invalidateQueryKey: ['workflowVersion'],
        options: { onSuccess },
    });
