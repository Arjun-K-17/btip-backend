def generate_report(company_id: int, analysis: dict) -> dict:
    return {
        "company_id": company_id,
        "report_title": "Business Turnaround Analysis Report",

        "financial_summary": {
            "profit_margin": analysis.get("profit_margin"),
            "current_ratio": analysis.get("current_ratio"),
            "debt_to_equity": analysis.get("debt_to_equity"),
            "net_cash_flow": analysis.get("net_cash_flow")
        },

        "report_status": "generated"
    }
    # Title
    story.append(
        Paragraph(
            "BTIP - Business Turnaround Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Company: {company_name}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    # Analytics
    story.append(
        Paragraph(
            "Financial Analysis",
            styles["Heading2"]
        )
    )

    for key, value in analytics.items():
        story.append(
            Paragraph(
                f"<b>{key.replace('_', ' ').title()}:</b> {value}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # Crisis
    story.append(
        Paragraph(
            "Crisis Analysis",
            styles["Heading2"]
        )
    )

    for key, value in crisis.items():
        story.append(
            Paragraph(
                f"<b>{key.replace('_', ' ').title()}:</b> {value}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # Recommendations
    story.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    if recommendations:
        for recommendation in recommendations:
            title = recommendation.get(
                "title",
                "Recommendation"
            )

            description = recommendation.get(
                "description",
                ""
            )

            story.append(
                Paragraph(
                    f"<b>{title}</b>: {description}",
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 5))
    else:
        story.append(
            Paragraph(
                "No recommendations available.",
                styles["BodyText"]
            )
        )

    document.build(story)

    return buffer.getvalue()