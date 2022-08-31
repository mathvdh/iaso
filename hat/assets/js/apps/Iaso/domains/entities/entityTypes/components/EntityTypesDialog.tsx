/* eslint-disable camelcase */
import React, { ReactNode, FunctionComponent, useState, useMemo } from 'react';
import { useFormik, FormikProvider, FormikProps } from 'formik';
import * as yup from 'yup';
import {
    // @ts-ignore
    useSafeIntl,
    // @ts-ignore
    IconButton as IconButtonComponent,
} from 'bluesquare-components';
import { makeStyles, Box } from '@material-ui/core';
import isEqual from 'lodash/isEqual';

import InputComponent from '../../../../components/forms/InputComponent';
import ConfirmCancelDialogComponent from '../../../../components/dialogs/ConfirmCancelDialogComponent';
import { IntlMessage } from '../../../../types/intl';
import { EntityType } from '../types/entityType';

import { baseUrls } from '../../../../constants/urls';

import { useGetForm, useGetForms } from '../hooks/requests/forms';

import MESSAGES from '../messages';

type RenderTriggerProps = {
    openDialog: () => void;
};

type EmptyEntityType = {
    name?: string;
    reference_form?: number;
    fields_detail_info_view?: string[];
    fields_list_view?: string[];
};

type Props = {
    titleMessage: IntlMessage;
    // eslint-disable-next-line no-unused-vars
    renderTrigger: ({ openDialog }: RenderTriggerProps) => ReactNode;
    initialData?: EntityType;
    // eslint-disable-next-line no-unused-vars
    saveEntityType: (e: EntityType) => void;
};

const useStyles = makeStyles(theme => ({
    root: {
        position: 'relative',
    },
    view: {
        position: 'absolute',
        top: theme.spacing(1),
        right: theme.spacing(1),
    },
}));

export const EntityTypesDialog: FunctionComponent<Props> = ({
    titleMessage,
    renderTrigger,
    initialData = {
        id: undefined,
        name: undefined,
        reference_form: undefined,
        fields_detail_info_view: [],
        fields_list_view: [],
    },
    saveEntityType,
}) => {
    const classes: Record<string, string> = useStyles();
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const { formatMessage } = useSafeIntl();

    const getSchema = () =>
        yup.lazy(() =>
            yup.object().shape({
                name: yup
                    .string()
                    .trim()
                    .required(formatMessage(MESSAGES.nameRequired)),
            }),
        );

    const formik: FormikProps<EntityType | EmptyEntityType> = useFormik<
        EntityType | EmptyEntityType
    >({
        initialValues: initialData,
        enableReinitialize: true,
        validateOnBlur: true,
        validationSchema: getSchema,
        onSubmit: saveEntityType,
    });
    const {
        values,
        setFieldValue,
        errors,
        isValid,
        initialValues,
        handleSubmit,
        resetForm,
    } = formik;
    const getErrors = k => (errors[k] ? [errors[k]] : []);
    const { data: currentForm, isFetching: isFetchingForm } = useGetForm(
        values?.reference_form,
        Boolean(values?.reference_form) && isOpen,
        'possible_fields',
    );
    const isNew = !initialData?.id;
    const { data: formsList, isFetching: isFetchingForms } = useGetForms(isNew);
    const possibleFields = useMemo(
        () =>
            (currentForm?.possible_fields || []).map(field => ({
                value: field.name,
                label: field.label,
            })),
        [currentForm],
    );
    return (
        <FormikProvider value={formik}>
            {/* @ts-ignore */}
            <ConfirmCancelDialogComponent
                allowConfirm={isValid && !isEqual(values, initialValues)}
                titleMessage={titleMessage}
                onConfirm={handleSubmit}
                onCancel={closeDialog => {
                    closeDialog();
                    resetForm();
                }}
                cancelMessage={MESSAGES.cancel}
                confirmMessage={MESSAGES.save}
                renderTrigger={renderTrigger}
                maxWidth="xs"
                dialogProps={{
                    classNames: classes.dialog,
                }}
                onOpen={() => setIsOpen(true)}
                onClosed={() => setIsOpen(false)}
            >
                {!isNew && (
                    <Box className={classes.view}>
                        <IconButtonComponent
                            url={`/${baseUrls.formDetail}/formId/${values.reference_form}`}
                            icon="remove-red-eye"
                            tooltipMessage={MESSAGES.viewForm}
                        />
                    </Box>
                )}
                <div className={classes.root} id="entity-types-dialog">
                    <InputComponent
                        keyValue="name"
                        onChange={setFieldValue}
                        value={values.name}
                        errors={getErrors('name')}
                        type="text"
                        label={MESSAGES.name}
                        required
                    />
                    {isNew && (
                        <InputComponent
                            keyValue="reference_form"
                            onChange={setFieldValue}
                            disabled={isFetchingForms}
                            loading={isFetchingForms}
                            value={values.reference_form || null}
                            type="select"
                            options={
                                formsList?.map(t => ({
                                    label: t.name,
                                    value: t.id,
                                })) || []
                            }
                            label={MESSAGES.referenceForm}
                        />
                    )}
                    <InputComponent
                        type="select"
                        multi
                        disabled={isFetchingForm || !values.reference_form}
                        keyValue="fields_list_view"
                        onChange={(key, value) =>
                            setFieldValue(key, value ? value.split(',') : null)
                        }
                        value={!isFetchingForm ? values.fields_list_view : []}
                        label={MESSAGES.fieldsListView}
                        options={possibleFields}
                    />
                    <InputComponent
                        type="select"
                        multi
                        disabled={isFetchingForm || !values.reference_form}
                        loading={isFetchingForm}
                        keyValue="fields_detail_info_view"
                        onChange={(key, value) =>
                            setFieldValue(key, value ? value.split(',') : null)
                        }
                        value={
                            !isFetchingForm
                                ? values.fields_detail_info_view
                                : []
                        }
                        label={MESSAGES.fieldsDetailInfoView}
                        options={possibleFields}
                    />
                </div>
            </ConfirmCancelDialogComponent>
        </FormikProvider>
    );
};
