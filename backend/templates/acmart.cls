\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{acmart}[2026/01/01 ACM Class]
\LoadClass[10pt,twocolumn,letterpaper]{article}
\RequirePackage[margin=0.75in]{geometry}
\newcommand{\acmConference}[4]{}
\newcommand{\acmBooktitle}[1]{}
\newcommand{\acmPrice}[1]{}
\newcommand{\acmDOI}[1]{}
\newcommand{\acmISBN}[1]{}
\newcommand{\acmYear}[1]{}
\newcommand{\copyrightyear}[1]{}
\newcommand{\setcopyright}[1]{}
\newcommand{\settopmatter}[1]{}
% Author topmatter. The real acmart accumulates \affiliation and \email into the
% author block; this stub previously defined neither, so a package that emits them
% (as acmart requires) failed with an undefined control sequence here while
% compiling fine at ACM. Append them to the author entry instead.
\makeatletter
\newcommand{\position}[1]{#1}
\newcommand{\institution}[1]{#1}
\newcommand{\department}[1]{#1}
\newcommand{\streetaddress}[1]{#1}
\newcommand{\city}[1]{#1}
\newcommand{\state}[1]{#1}
\newcommand{\postcode}[1]{#1}
\newcommand{\country}[1]{#1}
\newcommand{\orcid}[1]{}
\newcommand{\affiliation}[1]{\g@addto@macro\@author{\\ #1}}
\newcommand{\email}[1]{\g@addto@macro\@author{\\ \texttt{#1}}}
\newcommand{\keywords}[1]{}
\makeatother
