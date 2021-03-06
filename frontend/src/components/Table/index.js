// @flow
import React from 'react';
import type { Node } from 'react';
import styled from 'styled-components/macro';
import { dataTransformer } from './dataTransformer';
import type { MatchesType } from '../../types';

const StyledTable = styled.table`
  border-collapse: collapse;
  width: 100%;
`;

const StyledCaption = styled.caption`
  margin-bottom: .5rem;
  font-style: italic;
  text-align: left;
`;

const StyledTableHeading = styled.th`
font-weight: 700;
white-space: nowrap;
background: #fff;
color: #000;
border-bottom: 4px solid black;
padding: 0.5rem 0.75rem;
text-align: left;
`;

const StyledDataCell = styled.td`
border: 2px solid rgba(0,0,0,0.3);
padding: 0.75rem;
text-align: left;
`;

type Props = {
  caption: string,
  headers: Array<string>,
  rows: MatchesType
}

const Table = ({ caption, headers, rows }: Props): Node => {
  if (!rows || rows.length === 0) {
    return <div>Data not found</div>;
  }
  const rowsArray = dataTransformer(rows);

  return (
    <StyledTable>
      {caption && <StyledCaption>{caption}</StyledCaption>}
      <tbody>
        <tr>
          {
            headers && headers.length > 0 && headers.map(item => (
              <StyledTableHeading scope="col" key={item}>{item}</StyledTableHeading>
            ))
          }
        </tr>
        {
          rowsArray && rowsArray.length > 0 && rowsArray.map(row => (
            <tr key={Math.random()}>
              {row.map(value => (
                <StyledDataCell key={value}>{value}</StyledDataCell>
              ))}
            </tr>
          ))
        }
      </tbody>
    </StyledTable>
  );
};

export default Table;
