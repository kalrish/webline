# Parses configuration on behalf of integrations


require 'yaml'


def parse(yaml)
  config = YAML.safe_load(
    yaml,
  )

  return config
end


def validate(config)
  return true
end


def main(yaml)
  valid = False
  config = None

  parsing_messages = []

  begin
    config = parse(
      yaml,
    )
  rescue
    status = 'INVALID'
  else
    validation_messages = []

    response = validate(
      config,
    )
  end

  response = {
  }

  return response
end


def handler(event, context)
  yaml = event['YAML']

  response = main(
    yaml,
  )

  return response
end
