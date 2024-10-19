declare module 'react-katex' {
    import * as React from 'react';

    interface KatexProperties {
        math: string;
        errorColor?: string;
        renderError?: (error: Error) => React.ReactNode;
        throwOnError?: boolean;
    }

    export class InlineMath extends React.Component<KatexProperties, any> { }
    export class BlockMath extends React.Component<KatexProperties, any> { }
}