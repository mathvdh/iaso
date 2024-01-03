import React, { ReactNode, useState } from 'react';
import { Box } from '@mui/material';
import {
    TextInput,
    PasswordInput,
    NumberInput,
    Radio,
    Checkbox,
    ArrayFieldInput,
    SearchInput,
    // @ts-ignore
    translateOptions,
    Select,
    useSafeIntl,
    IntlMessage,
} from 'bluesquare-components';
import { useSelector } from 'react-redux';
import MESSAGES from '../../domains/forms/messages';
import { DropdownOptions } from '../../types/utils';

type Option = DropdownOptions<string | number>;

export type InputComponentType =
    | 'text'
    | 'email'
    | 'password'
    | 'number'
    | 'radio'
    | 'checkbox'
    | 'arrayInput'
    | 'search'
    | 'select';

export type NumberInputOptions = {
    min?: number;
    max?: number;
    decimalScale?: number;
    decimalSeparator?: '.' | ',';
    thousandSeparator?: '.' | ',';
};

export type Locale = {
    code: string;
    label: string;
};

export type InputComponentProps = {
    type: InputComponentType;
    keyValue: string;
    value?: any;
    errors?: string[];
    // eslint-disable-next-line no-unused-vars
    onChange?: (key: string, value: any) => void;
    options?: any[];
    disabled?: boolean;
    multiline?: boolean;
    clearable?: boolean;
    label?: IntlMessage;
    labelString?: string;
    required?: boolean;
    onEnterPressed?: () => void;
    withMarginTop?: boolean;
    multi?: boolean;
    uid?: string;
    loading?: boolean;
    // eslint-disable-next-line no-unused-vars
    getOptionLabel?: (option: Option) => string;
    getOptionSelected?: (
        // eslint-disable-next-line no-unused-vars
        option: Option,
        // eslint-disable-next-line no-unused-vars
        value: Option,
    ) => boolean;
    renderOption?: (
        // eslint-disable-next-line no-unused-vars
        option: Option,
        // eslint-disable-next-line no-unused-vars
        { inputValue }: { inputValue: string },
    ) => ReactNode;
    className?: string;
    helperText?: string;
    min?: number;
    max?: number;
    blockForbiddenChars?: boolean;
    onErrorChange?: () => void;
    numberInputOptions?: {
        min?: number;
        max?: number;
        decimalScale?: number;
        decimalSeparator?: '.' | ',';
        thousandSeparator?: '.' | ',';
    };
    // eslint-disable-next-line no-unused-vars
    setFieldError?: (keyValue: string, message: string) => void;
};

const determineSeparatorsFromLocale = (
    activeLocale: Locale,
): { thousand: '.' | ','; decimal: '.' | ',' } => {
    // using a switch to add more locales easily
    switch (activeLocale.code) {
        case 'fr':
            return { thousand: '.', decimal: ',' };
        case 'en':
            return { thousand: ',', decimal: '.' };
        default:
            return { thousand: ',', decimal: '.' };
    }
};

const determineNumberSeparators = (
    activeLocale: Locale,
    numberInputOptions: NumberInputOptions,
): NumberInputOptions => {
    const { thousand, decimal } = determineSeparatorsFromLocale(activeLocale);
    console.log('thousand', thousand, 'decimal', decimal);
    return {
        ...numberInputOptions,
        decimalSeparator: numberInputOptions?.decimalSeparator ?? decimal,
        thousandSeparator: numberInputOptions?.thousandSeparator ?? thousand,
    };
};

const InputComponent: React.FC<InputComponentProps> = ({
    type = 'text',
    keyValue,
    value,
    errors = [],
    onChange = () => null,
    options = [],
    disabled = false,
    multiline = false,
    clearable = true,
    label,
    labelString = null,
    required = false,
    onEnterPressed = () => null,
    withMarginTop = true,
    multi = false,
    uid,
    loading = false,
    getOptionLabel,
    getOptionSelected,
    renderOption,
    className = '',
    helperText,
    min,
    max,
    blockForbiddenChars = false,
    onErrorChange = () => null,
    numberInputOptions = {},
    setFieldError = () => null,
}) => {
    const [displayPassword, setDisplayPassword] = useState(false);
    const { formatMessage } = useSafeIntl();
    // @ts-ignore
    const activeLocale = useSelector(state => state.app.locale);
    const localizedNumberOptions = determineNumberSeparators(
        activeLocale,
        numberInputOptions,
    );
    console.log('active locale', activeLocale, numberInputOptions);
    console.log('LOCALOPTION', localizedNumberOptions);

    const toggleDisplayPassword = () => {
        setDisplayPassword(!displayPassword);
    };

    const inputValue =
        value === null || typeof value === 'undefined' ? '' : value;
    const labelText =
        typeof labelString === 'string'
            ? labelString
            : formatMessage(label || MESSAGES[keyValue]);
    const renderInput = () => {
        switch (type) {
            case 'email':
            case 'text':
                return (
                    <TextInput
                        value={inputValue}
                        keyValue={keyValue}
                        label={labelText}
                        errors={errors}
                        required={required}
                        multiline={multiline}
                        disabled={disabled}
                        onChange={input => {
                            onChange(keyValue, input);
                        }}
                    />
                );
            case 'password':
                return (
                    <PasswordInput
                        value={inputValue}
                        keyValue={keyValue}
                        errors={errors}
                        label={labelText}
                        required={required}
                        multiline={multiline}
                        disabled={disabled}
                        onChange={input => {
                            onChange(keyValue, input);
                        }}
                        onClick={toggleDisplayPassword}
                        displayPassword={displayPassword}
                        tooltipMessage={MESSAGES.displayPassword}
                    />
                );
            case 'number':
                return (
                    <NumberInput
                        min={min}
                        max={max}
                        value={inputValue}
                        keyValue={keyValue}
                        label={labelText}
                        errors={errors}
                        required={required}
                        multiline={multiline}
                        disabled={disabled}
                        onChange={input => {
                            onChange(keyValue, input);
                        }}
                        setFieldError={setFieldError}
                        // eslint-disable-next-line react/jsx-props-no-spreading
                        {...localizedNumberOptions}
                    />
                );
            case 'select':
                return (
                    <Select
                        errors={errors}
                        keyValue={keyValue}
                        label={labelText}
                        required={required}
                        disabled={disabled}
                        loading={loading}
                        clearable={clearable}
                        multi={multi}
                        value={value}
                        renderOption={renderOption}
                        getOptionLabel={getOptionLabel}
                        getOptionSelected={getOptionSelected}
                        options={translateOptions(options, formatMessage)}
                        onChange={newValue => {
                            onChange(keyValue, newValue);
                        }}
                        helperText={helperText}
                    />
                );
            case 'arrayInput':
                return (
                    <ArrayFieldInput
                        label={labelText}
                        fieldList={value}
                        name={keyValue}
                        baseId={keyValue}
                        updateList={list => onChange(keyValue, list)}
                    />
                );
            case 'search':
                return (
                    <SearchInput
                        uid={uid || ''}
                        keyValue={keyValue}
                        label={labelText}
                        required={required}
                        errors={errors}
                        disabled={disabled}
                        onEnterPressed={onEnterPressed}
                        onChange={newValue => onChange(keyValue, newValue)}
                        value={value}
                        blockForbiddenChars={blockForbiddenChars}
                        onErrorChange={onErrorChange}
                    />
                );
            case 'checkbox':
                return (
                    <Checkbox
                        keyValue={keyValue}
                        disabled={disabled}
                        onChange={newValue => onChange(keyValue, newValue)}
                        value={value}
                        label={labelText}
                        required={required}
                    />
                );
            case 'radio':
                return (
                    <Radio
                        className={className}
                        name={keyValue}
                        label={labelText}
                        error={errors}
                        onChange={newValue => onChange(keyValue, newValue)}
                        options={options}
                        value={value}
                        required={required}
                    />
                );
            default:
                return null;
        }
    };
    return <Box mt={withMarginTop ? 2 : 0}>{renderInput()}</Box>;
};

export default InputComponent;
