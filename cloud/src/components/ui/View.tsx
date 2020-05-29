import React from 'react'
import styled from 'styled-components'


export const Bubble = styled.div<{ shadow?: string }>`
    padding: 1rem;
    border-radius: ${p => p.theme.borderRadius};
    margin-bottom: 0.5rem;

    background-color: ${p => p.theme.colors.background.secondary};
    color: #222;

    h4 {
        font-size: 0.9rem;
        padding-bottom: 0.5rem;
        color: ${p => p.theme.colors.text.primary};
    }
`

export const ErrorBubble = styled(Bubble)`
    color: white;
    background-color: ${p => p.theme.colors.status.fail};
`

export const ContentBlock = styled.div`
    margin-bottom: 1.5rem;
`

export const Content = styled.div`
    padding: 1rem;
`

export const View: React.FC<{ title: string }> = ({ title, children }) => {
    return <div>
        <Content>
            {children}
        </Content>
    </div>
}
