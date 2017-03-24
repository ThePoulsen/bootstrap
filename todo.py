Todo
    masterData:

    intermediaries:
        rating
        event
        inheritedEvent
        valueChainStep
        project
        process
        organization
        pareto
        Risk

    end:
        eventRegistration

    n:n
        potentialEvent (risk/event)
        potentialTreatment (event/treatment)

make 10 different project data columns
program settings - name project data columns - enable/disable extra columns




done
    Intermediaries
        valueChain
        treatment
        causingFactor
        user
        group

    masterData:
        causingFactorType
        country
        deliveryPoint
        eventType
        likelihood
        processArea
        region
        riskArea
        riskResponse
        riskType
        severity
        status
        subRegion
        treatmentType
        valueChainArea
        valueChainStepType
        zone

create audit trail:
    table log
        id
        uuid
        timestamp
        user_uuid
        tenant_uuid
        table
        tableRow_uuid
        event
