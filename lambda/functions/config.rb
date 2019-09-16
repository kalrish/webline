# Parses configuration on behalf of integrations


require 'yaml'


def parse(yaml)
  config = YAML.safe_load(
    yaml,
  )

  return config
end


def handler(event, context)
  yaml = event['YAML']

  config = parse(
    yaml,
  )

  return config
end
