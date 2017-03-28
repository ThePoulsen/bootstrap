Todo
    masterData:

    intermediaries:
        event
        inheritedEvent
        valueChainStep
        project
        process
        organization
        pareto


    end:
        eventRegistration

    n:n
        potentialEvent (risk/event)
        potentialTreatment (event/treatment)

make 10 different project data columns
program settings - name project data columns - enable/disable extra columns




done
    User management
        user
        group

    Intermediaries
        valueChain
        treatment
        causingFactor
        rating
        rating matrix
        Risk

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
